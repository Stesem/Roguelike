#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Passage
{
    int *pattern;
    void *from;
    void *to;
} Passage;

typedef struct SqRoom
{
    int *pattern;
    char directions[4];
    Passage **passages;
} SqRoom;

// сверху структуры, снизу функции

int *RandomPattern() // твой random в питоне
{
    int *pattern = (int *)malloc(sizeof(int));
    *pattern = rand(); // random value for the pattern
    return pattern;
};

Passage **InitializePassage() // просто выделяем память для passage
{
    Passage **new_passage = (Passage **)malloc(4 * sizeof(Passage *));
    for (int i = 0; i < 4; i++)
    {
        new_passage[i] = (Passage *)malloc(sizeof(Passage));
        new_passage[i]->pattern = RandomPattern();
        new_passage[i]->from = NULL;
        new_passage[i]->to = NULL;
    }
    return new_passage;
}

SqRoom *InitializeRoom() // просто выделяем память для sqroom
{
    SqRoom *new_room = (SqRoom *)malloc(sizeof(SqRoom));
    new_room->pattern = RandomPattern();
    new_room->directions[0] = 'r';
    new_room->directions[1] = 'l';
    new_room->directions[2] = 'u';
    new_room->directions[3] = 'd';
    new_room->passages = InitializePassage();
    return new_room;
}

void CheckNeighbors(SqRoom ****graph, int index_j, int index_i, SqRoom **current_room)
{
    for (int current_direction = 0; current_direction < 4; ++current_direction)
    {
        SqRoom *neighbor = NULL;
        switch (current_direction)
        {
        case 0:                  // Right
            if (index_i + 1 < 4) // Assuming 4 is the grid size
                neighbor = (*graph)[index_j][index_i + 1];
            break;
        case 1: // Left
            if (index_i - 1 >= 0)
                neighbor = (*graph)[index_j][index_i - 1];
            break;
        case 2: // Up
            if (index_j - 1 >= 0)
                neighbor = (*graph)[index_j - 1][index_i];
            break;
        case 3:                  // Down
            if (index_j + 1 < 4) // Assuming 4 is the grid size
                neighbor = (*graph)[index_j + 1][index_i];
            break;
        }

        if (neighbor != NULL)
        {
            (*current_room)->passages[current_direction]->from = *current_room;
            (*current_room)->passages[current_direction]->to = neighbor;
            free(neighbor);
        }
    }
}

void CreateMap(bool **existing_table, struct SqRoom ***graph, int index_i, int index_j)
{
    if (graph[index_j][index_i])
    {
        return;
    }
    else if (!graph[index_j][index_i] && existing_table[index_j][index_i] == true)
    {
        graph[index_j][index_i] = InitializeRoom();
        CheckNeighbors(&graph, index_j, index_i, &graph[index_j][index_i]);

        if (index_i + 1 < 4)
            CreateMap(existing_table, graph, index_i + 1, index_j); // Right
        if (index_i - 1 >= 0)
            CreateMap(existing_table, graph, index_i - 1, index_j); // Left
        if (index_j - 1 >= 0)
            CreateMap(existing_table, graph, index_i, index_j - 1); // Up
        if (index_j + 1 < 4)
            CreateMap(existing_table, graph, index_i, index_j + 1); // Down
    }
    else
    {
        return;
    }
}

int main()
{
    printf("hello\n");
    return 0;
}