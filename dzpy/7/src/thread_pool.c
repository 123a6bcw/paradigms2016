#include "../include/thread_pool.h"

void list_init(struct List* list)
{
    list->head = NULL;
    pthread_mutex_init(&list->mutex, NULL);
    pthread_cond_init(&list->cond, NULL);
}

void list_finit(struct List* list)
{
    struct Node* fin;

    if (list->head == NULL)
    {
        return;
    }

    fin = list->head;
    do
    {
        free(list->head->task);
        list->head = list->head->r;
    } while (list->head != fin);

    pthread_mutex_destroy(&list->mutex);
    pthread_mutex_destroy(&list->mutex);
    pthread_cond_destroy(&list->cond);
}

void list_push(struct Node* n, struct List* list)
{
    pthread_mutex_lock(&list->mutex);
    
    if (list->head == NULL)
    {
        n->r = n;
        n->l = n;
        list->head = n;
    } else
    {
        n->r = list->head;
        n->l = list->head->l;
        list->head->l->r = n;
        list->head->l = n;
    }
    
    pthread_cond_signal(&list->cond);
    pthread_mutex_unlock(&list->mutex);
    return;
}

struct Task* list_pop(struct List* list)
{
    struct Task* ret;
    struct Node* new_head;
    
    if (list->head == NULL)
    {
        return NULL;
    }
    
    ret = list->head->task;
    new_head = list->head->r;
    
    if (list->head->r == list->head)
    {
        struct Task* ret = list->head->task;
        free(list->head);
        list->head = NULL;
        return ret;
    } else
    {
        new_head->l = list->head->l;
        list->head->l->r = new_head;
        free(list->head);
        list->head = new_head;
    }
    
    return ret;
}

void task_init(struct Task** task, int* a, size_t len, size_t steps_down, void (*f)(void *), struct ThreadPool* pool)
{
    struct SortTask* sort_task = malloc(sizeof(struct SortTask));
    sort_task->a = a;
    sort_task->len = len;
    sort_task->steps_down = steps_down;
    
    (*task) = malloc(sizeof(struct Task));
    (*task)->pool = pool;
    (*task)->f = f;
    (*task)->arg = (void*) sort_task;
    (*task)->finished = 0;
    (*task)->l = NULL;
    (*task)->r = NULL;
    
    sort_task->task = (*task);
    pthread_mutex_init(&(*task)->mutex, NULL);
    pthread_cond_init(&(*task)->cond, NULL);
    return;
}

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

void* worker(void* data)
{
    struct ThreadPool* pool = data;
    struct Task* task;
    
    while (pool->cont || pool->list.head != NULL)
    {
        pthread_mutex_lock(&pool->list.mutex);
        while (pool->cont && pool->list.head == NULL)
        {
            pthread_cond_wait(&pool->list.cond, &pool->list.mutex);
        }
        
        task = list_pop(&pool->list);
        pthread_mutex_unlock(&pool->list.mutex);
        
        if (task != NULL)
        {
            pthread_mutex_lock(&task->mutex);
            task->f(task->arg);
            task->finished = 1;
            pthread_cond_signal(&task->cond);
            pthread_mutex_unlock(&task->mutex);
        }
    }
    
    return NULL;
}

void thpool_init(struct ThreadPool* pool, size_t n)
{
    size_t i;
    list_init(&pool->list);
    pool->threads = malloc(n * sizeof(pthread_t));
    pool->n = n;
    pool->cont = 1;
    for (i = 0; i < n; i++)
    {
        pthread_create(&pool->threads[i], NULL, worker, pool);
    }
}

void thpool_submit(struct ThreadPool* pool, struct Task* task)
{
    struct Node *node = malloc(sizeof(struct Node));
    node->task = task;
    list_push(node, &pool->list);
}

void thpool_wait(struct Task* task)
{
    if (task == NULL)
    {
        return;
    }
    
    pthread_mutex_lock(&task->mutex);
    while (!task->finished)
    {
        pthread_cond_wait(&task->cond, &task->mutex);
    }
    
    pthread_mutex_unlock(&task->mutex);
}

void thpool_finit(struct ThreadPool* pool)
{
    size_t i;
    pthread_mutex_lock(&pool->list.mutex);
    pool->cont = 0;
    pthread_mutex_unlock(&pool->list.mutex);
    pthread_mutex_lock(&pool->list.mutex);
    pthread_cond_broadcast(&pool->list.cond);
    pthread_mutex_unlock(&pool->list.mutex);
    
    for (i = 0; i < pool->n; i++)
    {
        pthread_join(pool->threads[i], NULL);
    }
    
    free(pool->threads);
    list_finit(&pool->list);
}
