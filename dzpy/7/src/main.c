#include "../include/thread_pool.h"

void wait_sort(struct ThreadPool* pool, struct Task* task)
{
    if (task == NULL)
    {
        return;
    }
    
    thpool_wait(task);
    wait_sort(pool, task->l);
    wait_sort(pool, task->r);
}

void free_sort(struct Task* task)
{
    if (task == NULL)
    {
        return;
    }

    free_sort(task->l);
    free_sort(task->r);
    free((struct SortTask*)task->arg);
    pthread_mutex_destroy(&task->mutex);
    pthread_cond_destroy(&task->cond);
    free(task);
}

int main(int argc, char* argv[])
{
    size_t n_pools, n, rec_limit, i;
    int* a;
    int well_done;
    struct ThreadPool pool;
    struct Task* task = NULL;
    
    if (argc < 3)
    {
        printf("Whops\n");
    }
    
    srand(42);
    n_pools = atoi(argv[1]), n = atoi(argv[2]), rec_limit = atoi(argv[3]);
    a = malloc(n * sizeof(int));
    for (i = 0; i < n; i++)
    {
        a[i] =rand();
    }
    
    pool.list.head = NULL;
    thpool_init(&pool, n_pools);
    task_init(&task, a, n, rec_limit, sorting, &pool);
    thpool_submit(&pool, task);
    wait_sort(&pool, task);
    free_sort(task);
    thpool_finit(&pool);
    well_done = 1;
    for (i = 0; i + 1 < n; i++)
    {
        if (a[i] > a[i + 1])
        {
            well_done = 0;
        }
    }
    
    if (well_done)
    {
        printf("Well done!\n");
    } else
    {
        size_t i;
        for (i = 0; i < n; i++)
        {
            printf("%i ", a[i]);
            printf("\n");
        }
        printf("Not well done :(\n");
    }
    
    free(a);
    return 0;
}
