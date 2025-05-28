#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>

#define MAX_TITULO 100
#define MAX_PRIORIDADE 10
#define MAX_HORARIO 6
#define MAX_DATA 11

// Estrutura de usuários fixos
typedef struct {
    char nome[50];
    char senha[50];
} Usuario;

Usuario usuarios[] = {
    {"matheus", "senha123"},
    {"marcos", "123marcos"},
    {"miguel", "miguel2024"}
};
int total_usuarios = sizeof(usuarios) / sizeof(usuarios[0]);

// Estrutura de tarefa
typedef struct Tarefa {
    int id;
    char titulo[MAX_TITULO];
    int concluida;
    char prioridade[MAX_PRIORIDADE];
    char horario[MAX_HORARIO];
    char data_criacao[MAX_DATA];
    char data_prevista[MAX_DATA];
    struct Tarefa* prox;
} Tarefa;

// Função de login com múltiplos usuários
int login() {
    char username[50], password[50];

    printf("\nLogin\n");
    printf("Usuário: ");
    fgets(username, sizeof(username), stdin);
    username[strcspn(username, "\n")] = 0;

    printf("Senha: ");
    fgets(password, sizeof(password), stdin);
    password[strcspn(password, "\n")] = 0;

    for (int i = 0; i < total_usuarios; i++) {
        if (strcmp(username, usuarios[i].nome) == 0 && strcmp(password, usuarios[i].senha) == 0) {
            return 1;
        }
    }

    printf("\nUsuário ou senha inválidos.\n");
    return 0;
}

// Validação e correção de horário
int corrigirHorario(const char* entrada, char* saida) {
    char digitos[5] = {0};
    int count = 0;
    for (int i = 0; entrada[i] != '\0' && count < 4; i++) {
        if (isdigit(entrada[i])) {
            digitos[count++] = entrada[i];
        }
    }
    if (count != 4) return 0;
    sprintf(saida, "%c%c:%c%c", digitos[0], digitos[1], digitos[2], digitos[3]);
    return 1;
}

void obterDataFormatada(char* destino, int dias_adicionais) {
    time_t t = time(NULL) + dias_adicionais * 86400;
    struct tm tm = *localtime(&t);
    sprintf(destino, "%02d/%02d/%04d", tm.tm_mday, tm.tm_mon + 1, tm.tm_year + 1900);
}

Tarefa* criarTarefa(int id, const char* titulo, int concluida, int nivel_prioridade, const char* horario) {
    Tarefa* nova = (Tarefa*)malloc(sizeof(Tarefa));
    if (!nova) {
        printf("Erro ao alocar memória!\n");
        return NULL;
    }

    nova->id = id;
    strncpy(nova->titulo, titulo, MAX_TITULO);
    nova->concluida = concluida;
    strncpy(nova->horario, horario, MAX_HORARIO);
    nova->prox = NULL;

    switch (nivel_prioridade) {
        case 1:
            strcpy(nova->prioridade, "Alta");
            obterDataFormatada(nova->data_prevista, 1);
            break;
        case 2:
            strcpy(nova->prioridade, "Média");
            obterDataFormatada(nova->data_prevista, 3);
            break;
        case 3:
            strcpy(nova->prioridade, "Baixa");
            obterDataFormatada(nova->data_prevista, 7);
            break;
        default:
            strcpy(nova->prioridade, "Desconhecida");
            obterDataFormatada(nova->data_prevista, 0);
    }

    obterDataFormatada(nova->data_criacao, 0);
    return nova;
}

void adicionarTarefa(Tarefa** lista, Tarefa* nova) {
    if (strcmp(nova->prioridade, "Alta") == 0) {
        Tarefa* temp = *lista;
        while (temp != NULL) {
            temp->id++;
            temp = temp->prox;
        }
        nova->prox = *lista;
        *lista = nova;
    } else {
        if (*lista == NULL) {
            *lista = nova;
        } else {
            Tarefa* temp = *lista;
            while (temp->prox != NULL) {
                temp = temp->prox;
            }
            temp->prox = nova;
        }
    }
}

void listarTarefas(Tarefa* lista) {
    if (lista == NULL) {
        printf("\nNenhuma tarefa cadastrada!\n");
        return;
    }
    Tarefa* temp = lista;
    while (temp != NULL) {
        printf("\nID: %d | Título: %s\nPrioridade: %s | Horário: %s\nStatus: %s",
               temp->id, temp->titulo, temp->prioridade, temp->horario,
               temp->concluida ? "Concluída" : "Pendente");
        printf("\nCriada em: %s | Previsão: %s\n", temp->data_criacao, temp->data_prevista);
        temp = temp->prox;
    }
}

void atualizarTarefa(Tarefa* lista, int id) {
    Tarefa* temp = lista;
    while (temp != NULL && temp->id != id) {
        temp = temp->prox;
    }
    if (temp == NULL) {
        printf("\nID da tarefa não encontrado!\n");
        return;
    }

    int acao;
    printf("\n1 - Atualizar título\n2 - Marcar como concluída\nEscolha: ");
    scanf("%d", &acao);
    getchar();

    switch (acao) {
        case 1:
            printf("Novo título: ");
            fgets(temp->titulo, MAX_TITULO, stdin);
            temp->titulo[strcspn(temp->titulo, "\n")] = 0;
            printf("? Título atualizado!\n");
            break;
        case 2:
            temp->concluida = 1;
            printf("? Tarefa marcada como concluída!\n");
            break;
        default:
            printf("? Opção inválida.\n");
    }
}

void removerTarefa(Tarefa** lista, int id) {
    Tarefa *atual = *lista, *anterior = NULL;
    while (atual != NULL && atual->id != id) {
        anterior = atual;
        atual = atual->prox;
    }

    if (atual == NULL) {
        printf("? Tarefa com ID %d não encontrada.\n", id);
        return;
    }

    if (anterior == NULL) {
        *lista = atual->prox;
    } else {
        anterior->prox = atual->prox;
    }

    free(atual);
    printf("? Tarefa deletada com sucesso!\n");
}

void filtrarTarefas(Tarefa* lista) {
    int tipo;
    printf("\nFiltrar por:\n1 - Prioridade\n2 - Status\nEscolha: ");
    scanf("%d", &tipo);
    getchar();

    if (tipo == 1) {
        char filtro[MAX_PRIORIDADE];
        printf("Digite a prioridade para filtrar (Alta, Média, Baixa): ");
        fgets(filtro, MAX_PRIORIDADE, stdin);
        filtro[strcspn(filtro, "\n")] = 0;

        Tarefa* temp = lista;
        int encontrou = 0;
        while (temp != NULL) {
            if (strcmp(temp->prioridade, filtro) == 0) {
                printf("\nID: %d | Título: %s | Prioridade: %s | Horário: %s | Status: %s",
                       temp->id, temp->titulo, temp->prioridade, temp->horario,
                       temp->concluida ? "Concluída" : "Pendente");
                printf("\nCriada em: %s | Previsão: %s\n", temp->data_criacao, temp->data_prevista);
                encontrou = 1;
            }
            temp = temp->prox;
        }
        if (!encontrou) printf("\nNenhuma tarefa com essa prioridade.\n");

    } else if (tipo == 2) {
        int status;
        printf("Filtrar por:\n0 - Pendente\n1 - Concluída\nEscolha: ");
        scanf("%d", &status);
        getchar();

        Tarefa* temp = lista;
        int encontrou = 0;
        while (temp != NULL) {
            if (temp->concluida == status) {
                printf("\nID: %d | Título: %s | Prioridade: %s | Horário: %s | Status: %s",
                       temp->id, temp->titulo, temp->prioridade, temp->horario,
                       temp->concluida ? "Concluída" : "Pendente");
                printf("\nCriada em: %s | Previsão: %s\n", temp->data_criacao, temp->data_prevista);
                encontrou = 1;
            }
            temp = temp->prox;
        }
        if (!encontrou) printf("\nNenhuma tarefa com esse status.\n");
    } else {
        printf("? Opção de filtro inválida.\n");
    }

    printf("\nPressione Enter para continuar...");
    getchar();
}

void liberarLista(Tarefa* lista) {
    Tarefa* temp;
    while (lista != NULL) {
        temp = lista;
        lista = lista->prox;
        free(temp);
    }
}

// Função principal
int main() {
    Tarefa* lista = NULL;
    int idAtual = 1;
    int opcao;
    int rodando = 1;

    if (!login()) {
        return 0;
    }

    while (rodando) {
        printf("\n======================================\n");
        printf("        GERENCIADOR DE TAREFAS        \n");
        printf("======================================\n");
        printf("1 - Adicionar Tarefa\n");
        printf("2 - Listar Tarefas\n");
        printf("3 - Atualizar Tarefa\n");
        printf("4 - Deletar Tarefa\n");
        printf("5 - Sair\n");
        printf("6 - Filtrar Tarefas\n");
        printf("======================================\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);
        getchar();

        switch (opcao) {
            case 1: {
                char titulo[MAX_TITULO], entrada_horario[20], horario_corrigido[MAX_HORARIO];
                int nivel_prioridade;
                printf("\nDigite o título da tarefa: ");
                fgets(titulo, MAX_TITULO, stdin);
                titulo[strcspn(titulo, "\n")] = 0;

                printf("Escolha a prioridade:\n1 - Alta (24h)\n2 - Média (3 dias)\n3 - Baixa (7 dias)\nEscolha: ");
                scanf("%d", &nivel_prioridade);
                getchar();

                while (1) {
                    printf("Digite o horário (ex: 0930 ou 09:30): ");
                    fgets(entrada_horario, sizeof(entrada_horario), stdin);
                    entrada_horario[strcspn(entrada_horario, "\n")] = 0;

                    if (corrigirHorario(entrada_horario, horario_corrigido)) {
                        break;
                    } else {
                        printf("? Horário inválido! Digite algo como 0930 ou 09:30.\n");
                    }
                }

                Tarefa* nova = criarTarefa(idAtual++, titulo, 0, nivel_prioridade, horario_corrigido);
                adicionarTarefa(&lista, nova);
                printf("? Tarefa adicionada com sucesso!\n");
                break;
            }

            case 2:
                listarTarefas(lista);
                printf("\nPressione Enter para continuar...");
                getchar();
                break;

            case 3: {
                int id;
                printf("Digite o ID da tarefa para atualizar: ");
                scanf("%d", &id);
                getchar();
                atualizarTarefa(lista, id);
                break;
            }

            case 4: {
                int id;
                printf("Digite o ID da tarefa para deletar: ");
                scanf("%d", &id);
                getchar();
                removerTarefa(&lista, id);
                break;
            }

            case 5:
                rodando = 0;
                break;

            case 6:
                filtrarTarefas(lista);
                break;

            default:
                printf("? Opção inválida!\n");
        }
    }

    liberarLista(lista);
    printf("?? Saindo do programa...\n");
    return 0;
}
