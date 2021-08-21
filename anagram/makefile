test: main.o anagram.o
	cc -o test main.o anagram.o

main.o: main.c anagram.h
anagram.o: anagram.c anagram.h

clean:
	rm -f *.o test
