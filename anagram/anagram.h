#ifndef ANAGRAM_H
#define ANAGRAM_H

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define YES (1)
#define NO (0)
#define ERR (-1)

/* don't touch this structure directly */
typedef struct _anagram_t {
    int len;
    char *base;
    char *prev;
} ANAGRAM;


ANAGRAM *new_anagram(const char *base);
void set_prev(ANAGRAM *a, const char *prev);

ANAGRAM *new_anagram_with_len(const char *base, int len);

/* return NULL if error. return 0 length str when end */
char *anagram(ANAGRAM *a);
void delete_anagram(ANAGRAM *a);

#endif /* ANAGRAM_H */