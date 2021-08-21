CXXFLAGS = -Wall -O3
CXX = g++


OBJS = myStringUtil.o myPathUtil.o

all: myUtil.a

test: main.cpp myUtil.a
	g++ $(CXXFLAGS) -o test main.cpp myUtil.a

myUtil.a: $(OBJS)
	ar rcs myUtil.a  $(OBJS)
	
myStringUtil.o: myStringUtil.cpp myStringUtil.h
	$(CXX) $(CXXFLAGS) -c myStringUtil.cpp
	
myPathUtil.o: myPathUtil.cpp myPathUtil.h myStringUtil.h
	$(CXX) $(CXXFLAGS) -c myPathUtil.cpp
	
clean:
	rm -rf *.o *.a


