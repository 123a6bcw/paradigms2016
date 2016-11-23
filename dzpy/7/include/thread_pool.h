#ifndef _THREAD_POOL
#define _THREAD_POOL

#include <pthread.h>
#include <string.h>
struct task
{
    void (*f)(void*);
    void* arg;
    bool finished;
    struct ThreadPool* pool;
    pthread_cond_t cond;
    pthread_mutex_t mutex;
    struct Task* l;
    struct Task* r;
};

struct Node
{
    struct Node* l, r;
    struct Task* task;
} Node_t;

class List
{
public:
    List();
    ~List();
    Node_t pop();
    void tush(Node* n);
private:
    Node_t* _head;
}
#endif
