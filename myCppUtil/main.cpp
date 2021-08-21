


#include <iostream>
#include <cctype>
#include <functional>
#include <string>

#include "myStringUtil.h"
#include "myPathUtil.h"



struct isSpace : std::unary_function<const char &, bool> {
// struct isSpace : public sh::unaryPredicate {
	bool operator()(const char & c) {
		return isspace(c);
	}	
};


using sh::path::Path;

struct add_prefix : std::unary_function<Path, int> {
	std::string prefix;
	add_prefix(const std::string & __prefix) : prefix(__prefix) {
		
	};
	
	int operator()(const Path & path) {
		Path new_name(prefix + path.basename().str());
		Path new_path = path.dirname() + new_name;
		
		return sh::path::rename(path, new_path); 
	}
};


int main(void) {
	std::string str = "a b c";
	
	std::vector<std::string> v;
	// isSpace a;
	sh::split(v, str, isSpace());
	// sh::split(v, str, isspace);
	// sh::split(v, str, 'b');
	
	
	for (unsigned int i = 0; i < v.size(); i++) {
		std::cout << '"' << v[i] << '"' << std::endl;	
	}
	
	std::string str2 = sh::join(v, 1);
	
	std::cout << str2 << std::endl;
	
	std::vector<int> v2;
	v2.push_back(1);
	v2.push_back(2);
	v2.push_back(3);
	
	std::cout << sh::join(v2, ":") << std::endl;
	// std::string buf("");
	// int x = 3;
	
	std::string str3 = "     x y     ";
	std::cout << '"' << sh::lstrip(str3) << '"' << std::endl;
	std::cout << '"' << sh::rstrip(str3) << '"' << std::endl;
	std::cout << '"' << sh::strip(str3) << '"' << std::endl;
	
	
	str3 = "x y";
	std::cout << '"' << sh::lstrip(str3) << '"' << std::endl;
	std::cout << '"' << sh::rstrip(str3) << '"' << std::endl;
	std::cout << '"' << sh::strip(str3) << '"' << std::endl;
	
	str3 = "     ";
	std::cout << "l" << '"' << sh::lstrip(str3) << '"' << std::endl;
	std::cout << "r" << '"' << sh::rstrip(str3) << '"' << std::endl;
	std::cout << "s" << '"' << sh::strip(str3) << '"' << std::endl;
	
	str3 = "";
	std::cout << '"' << sh::lstrip(str3) << '"' << std::endl;
	std::cout << '"' << sh::rstrip(str3) << '"' << std::endl;
	std::cout << '"' << sh::strip(str3) << '"' << std::endl;

	str3 = "aabbaa";
	std::cout << '"' << sh::lstrip(str3,'a') << '"' << std::endl;
	std::cout << '"' << sh::rstrip(str3, 'a') << '"' << std::endl;
	std::cout << '"' << sh::strip(str3, 'a') << '"' << std::endl;


	Path path("/dir/base");
	
	std::cout << path << std::endl;
	
	std::cout << path.basename() << std::endl;
	std::cout << path.dirname() << std::endl;
	
	path = Path("base");
	
	std::cout << path << std::endl;
	std::cout << path.basename() << std::endl;
	std::cout << path.dirname() << std::endl;
	
	Path path1("dir/");
	Path path2("/dir2/");
	Path path3("dir3");
	Path path4("/dir4");
	Path path5("file");
	
	std::cout << path1 + path2 + path3 + path4 + path5 << std::endl;
	
	// Path olddir("dir");
	// Path newdir("newdir");
	// sh::path::rename(olddir, newdir);
	{
		Path path("work");
		
		int r = sh::path::traverse(path, add_prefix("prefix_"));
		// int r = sh::path::remove_all(path);
		if (r < 0) {
			std::cerr << "Error: sh::path::remove_all : " << path << std::endl;
		}
	}

	return 0;	
}