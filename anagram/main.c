#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "anagram.h"

int main(int argc, char *argv[])
{
    char *base;
    char *buf;
    int len;
    ANAGRAM *a;

    if (argc == 2) {
        base = argv[1];
        a = new_anagram(base);
        buf = anagram(a);
        printf("%s", buf);
        free(buf);
        while (fgetc(stdin) != EOF) {
            buf = anagram(a);
            printf("%s", buf);
            free(buf);
        }
        delete_anagram(a);
    } else if (argc == 3) {
        base = argv[1];
        len = atoi(argv[2]);
        a = new_anagram_with_len(base, len);
        buf = anagram(a);
        printf("%s", buf);
        free(buf);
        while (fgetc(stdin) != EOF) {
            buf = anagram(a);
            printf("%s", buf);
            free(buf);
        }
        delete_anagram(a);
    }
    
    
    return 0;
}

