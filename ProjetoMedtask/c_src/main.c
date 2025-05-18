#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_TITULO 100
#define MAX_PRIORIDADE 10
#define MAX_HORARIO 6
#define MAX_DATA 11

typedef struct Tarefa {
    int id;
    char titulo[MAX_TITULO];
    char prioridade[MAX_PRIORIDADE];
    char horario[MAX_HORARIO];
    char data_criacao[MAX_DATA];
    char data_prevista[MAX_DATA];
    int concluida;
    struct Tarefa* prox;
} Tarefa;

// Exemplo simples de listagem
void listarTarefas() {
    printf("Funcao listarTarefas em C
");
}

int main() {
    listarTarefas();
    return 0;
}
