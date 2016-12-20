#include "../include/thread_pool.h"

int comp(const void* a, const void* b)
{
    return (*(int*)a - *(int*)b);
}

void sorting(void* arg)
{
    int* a;
    int x;
    int i, j;
    
    struct Task* t1 = NULL;
    struct Task* t2 = NULL;
    
    struct SortTask* sort_task = arg;
    
    if (sort_task->len <= 1)
    {
        return;
    }
    
    if (sort_task->steps_down == 0)
    {
        qsort(sort_task->a, sort_task->len, sizeof(int), comp);
        return;
    }
    
    a = sort_task->a;
    x = a[(sort_task->len) / 2];
    i = 0; 
    j = sort_task->len - 1;
    while (i <= j)
    {
        while (a[i] < x) i++;
        while (a[j] > x) j--;
        if (i <= j)
        {
            int swap = a[i];
            a[i] = a[j];
            a[j] = swap;
            i++;
            j--;
        }
    }
    
    task_init(&t1, a, j + 1, sort_task->steps_down - 1, sorting, sort_task->task->pool);
    task_init(&t2, a + i, sort_task->len - i, sort_task->steps_down - 1, sorting, sort_task->task->pool);
    sort_task->task->l = t1;
    sort_task->task->r = t2;
    thpool_submit(sort_task->task->pool, t1);
    thpool_submit(sort_task->task->pool, t2);
}

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
