#ifndef _THREAD_POOL
#define _THREAD_POOL

#include <stddef.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

struct Task
{
    void (*f)(void*);
    void* arg;
    int finished;

    struct Task* l;
    struct Task* r;
    
    pthread_cond_t cond;
    pthread_mutex_t mutex;
    struct ThreadPool* pool;
};

struct SortTask
{
    size_t len, steps_down;
    int *a;
    struct Task* task;
};

struct Node
{
    struct Node* l;
    struct Node* r;
    struct Task* task;
};

struct List
{
    struct Node* head;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
};

struct ThreadPool
{
    struct List list;
    pthread_t* threads;
    size_t n;
    int cont;
};

void task_init(struct Task** task, int* a, size_t len, size_t steps_down, void (*f)(void *), struct ThreadPool*);

void thpool_init(struct ThreadPool* pool, size_t n_pools);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_finit(struct ThreadPool* pool);
#endif
