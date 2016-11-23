#include "../include/thread_pool.h"

List::List()
{
    _head = NULL;
}

List::~List()
{
    Node_t* fin = _head;
    do
    {
        free(_head->task)
        _head = _head->r;
    } while (_head != fin);
}

void List::push(Node_t* n)
{
    if (_head == NULL)
    {
        n->r = n;
        n->l = n;
        _head = n;
        return;
    }
    
    n->r = _head;
    n->l = _head->prev;
    _head->l = n;
    _head->l->r = n;
    return;
}

Task* List::pop()
{
    if (_head == NULL)
    {
        return NULL;
    }
    
    if (_head->r == _head)
    {
        Node_t* ret = _head;
        _head = NULL;
        return ret->task;
    }
    
    Node_t* ret = _head;
    Node_t* new_head = _head->r;
    new_head->l = _head->l;
    _head->l->r = new_head;
    _head = new_head;
    return ret->task
}
