#include <string>
#include <iostream>

#include <vector>

#include "myStringUtil.h"

namespace sh {

	struct isSpace : std::unary_function<const char &, bool> {
	// struct isSpace : public sh::unaryPredicate {
		bool operator()(const char & c) {
			return isspace(c);
		}	
	};

	struct isChar : std::unary_function<const char &, bool> {
		isChar(char __c) : _c(__c)  { };

		bool operator()(const char & c) {
			return _c == c;
		}
		
	private:
		isChar() {};
		
		char _c;
	};



	void split(const std::string & str, std::vector<std::string> & strs)
	{
		split(strs, str, isSpace());
	}


	void split(const std::string & str, std::vector<std::string> & strs, char c)
	{
		split(strs, str, isChar(c));
	}

	void split(std::vector<std::string> & strs, const std::string & str)
	{
		split(strs, str, isSpace());
	}


	void split(std::vector<std::string> & strs, const std::string & str, const char c)
	{
		split(strs, str, isChar(c));
	}

	std::string lstrip(const std::string & str)
	{
		return lstrip(str, isSpace());
	}

	std::string lstrip(const std::string & str, const char c)
	{
		return lstrip(str, isChar(c));
	}

	std::string rstrip(const std::string & str)
	{
		return rstrip(str, isSpace());
	}

	std::string rstrip(const std::string & str, const char c)
	{
		return rstrip(str, isChar(c));
	}

	std::string strip(const std::string & str)
	{
		return strip(str, isSpace());
	}

	std::string strip(const std::string & str, const char c)
	{
		return strip(str, isChar(c));
	}

} // namespace sh