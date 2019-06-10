#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

int counter;
int ITER;
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;

void* f(void *arg)
{

    for(int i=0;i<ITER;i++)
    {
        pthread_mutex_lock(&mutex1);
        ++counter;
        pthread_mutex_unlock(&mutex1);

    }
    return 0;
}

int main(int argc, char *argv[])
{
    if(argc==3)
    {
        int N = atoi(argv[1]);
        ITER = atoi(argv[2]);

        pthread_t  *id_array;
        id_array = (pthread_t*)malloc(sizeof(pthread_t)*N);
        
        for(long j=0;j<N;j++)
        {
          pthread_create (&id_array[j], NULL, &f,(void*)j);
        }
        
        for(long k=0;k<N;k++)
        {
            pthread_join(id_array[k], NULL);
        }
        
        printf("\n\n %d \n\n", counter);
        exit(EXIT_SUCCESS);
    }
    else
    {
        perror(stderr, "Zla liczba argumentow");
        return 1;
    }
}
