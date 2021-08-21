#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "anagram.h"

static int chrcmp(char c1, char c2)
{
    char str1[2], str2[2];
    int result;
    
    str1[0] = tolower(c1);
    str1[1] = '\0';
    str2[0] = tolower(c2);
    str2[1] = '\0';
    result = strcmp(str1, str2);
    if (result == 0) {
        str1[0] = c1;
        str2[0] = c2;
        return strcmp(str1, str2);
    }
    return result;
}

static void i_sort(char a[], int n)
{
    int i, j;
    int w;
    
    for (i = 1; i < n; i++) {
        w = a[i];
        j = i-1;
        while (j >= 0 && chrcmp(w , a[j]) < 0) {
            a[j+1] = a[j];
            j--;
        }
        a[j+1] = w;
    }
}

/* str must be sorted */
/* return string of unifyed char */
static char *unifystr(const char *str, int len)
{
    int i;
    int count;
    char *result = malloc(sizeof(char) * (len + 1));
    
    if (result == NULL) {
        return NULL;
    }
    count = 0;
    result[0] = str[0];
    for (i = 1; i < len; i++) {
        if (result[count] != str[i]) {
            result[++count] = str[i];
        }
    }
    result[++count] = '\0';
    
    return result;
}

/* return string deleted one c of str */
static char *delete_c(const char *str, int len, int c)
{
    int i, j;
    int count;
    char *result = malloc(sizeof(char) * len);
    
    if (result == NULL) {
        return NULL;
    }
    
    j = 0;
    count = 1;
    for (i = 0; i < len; i++) {
        if (c == str[i] && count == 1) {
            count++;
            continue;
        }
        result[j++] = str[i];
    }
    result[j] = '\0';
    
    return result;
}

static int anagram_search(const char *base, int len, char *buf, int depth, const char *next, const char *prev, int *search_next)
{
    char *tmp;
    char *u_next;
    char u_next_len;
    int i;
    int find;
    
    /* printf("buf = %s\n", buf); */
    
    if (depth >= len && prev[0] == '\0') {
        /* generate first */
        return YES;
    } else if (depth >= len && strcmp(prev, buf) == 0) {
        /* find prev but not next*/
        *search_next = YES;
        return NO;
    } else if (depth >= len) {
        /* find next */
        return YES;
    }
    
    if ((u_next = unifystr(next, strlen(next))) == NULL) {
        return ERR;
    }
    
    if (prev[0] == '\0' || *search_next == YES) {
        i = 0;
    } else if (*search_next == NO) {
        u_next_len = strlen(u_next);
        for (i = 0; i < u_next_len; i++) {
            if (u_next[i] == prev[depth]) {
                break;
            }
        }
    }
    while (u_next[i] != '\0') {
        buf[depth] = u_next[i++];
        
        if((tmp = delete_c(next, strlen(next), buf[depth])) == NULL) {
            free(u_next);
            return NULL;
        }
        
        buf[depth + 1] = '\0';
        if ((find = anagram_search(base, len, buf, depth + 1, tmp, prev, search_next)) == YES) {
            free(u_next);
            free(tmp);
            return YES;
        } else if (find == ERR) {
            free(u_next);
            free(tmp);
            return ERR;
        }
        free(tmp);
    }
    free(u_next);
    return NO;
}

/* base must be sorted and pattern of next must be same as base */
static int next_anagram(const char *base, int len, const char *prev, char *buf)
{
    int search_next;
    int result;
    
    buf[0] = '\0';
    
    search_next = NO;
    result = anagram_search(base, len, buf, 0, base, prev, &search_next);
    
    return result;
}

ANAGRAM *new_anagram(const char *base)
{
    int len;
    ANAGRAM *new;
    char *base_buf;
    char *prev_buf;
    
    if (base == NULL) {
        return NULL;
    }
    
    len = strlen(base);
    if ((base_buf = malloc(sizeof(char) * (len + 1))) == NULL) {
        return NULL;
    }

    if ((prev_buf = malloc(sizeof(char) * (len + 1))) == NULL) {
        free(base_buf);
        return NULL;
    }
    
    if ((new = malloc(sizeof(ANAGRAM))) == NULL) {
        free(base_buf);
        free(prev_buf);
        return NULL;
    }
    strcpy(base_buf, base);
    i_sort(base_buf, len);
    prev_buf[0] = '\0';
    new->len = len;
    new->base = base_buf;
    new->prev = prev_buf;
    return new;
}

ANAGRAM *new_anagram_with_len(const char *base, int len)
{
    ANAGRAM *new;
    
    if ((new = new_anagram(base)) == NULL) {
        return NULL;
    }
    new->len = len;
    
    return new;
}

void set_prev(ANAGRAM *a, const char *prev)
{
    strcpy(a->prev, prev);
}

/* return NULL if error. return 0 length str when end */
char *anagram(ANAGRAM *a)
{
    char *buf;
    int result;
    
    if ((buf = malloc(sizeof(char) * (a->len + 1))) == NULL) {
        return NULL;
    }
    
    result = next_anagram(a->base, a->len, a->prev, buf);
    if (result == NO) {
        buf[0] = '\0';
    } else if (result == ERR) {
        free(buf);
        return NULL;
    }
    strcpy(a->prev, buf);
    return buf;
}

void delete_anagram(ANAGRAM *a)
{
    free(a->base);
    free(a->prev);
    free(a);
}


