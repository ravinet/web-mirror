#include <fstream>
#include <string>
#include <map>
#include <iostream>
#include <sstream>
using namespace std;
int main()  {
  std::string a;
  std::string f;
  std::string i;
  std::string no_num;
  std::string resource_file;
  std::string resource = "resource";
  std::string full_name;
  int count=0;
  int n;
  int q;
  int space;
  typedef std::map<std::string,std::string> mapT;
  mapT resource_map;
  std::stringstream sstm; 
  ifstream file;
  file.open("/home/ravinent/web-mirror/tempgets.txt");
  while(!file.eof())
  {
    if (file.fail()) {
      return(0);
    }
    getline(file, a);
    //find // and eliminate all before it (http:// or https)
    n = a.find("//");
    i = a.substr(n+2);
    //if first entry, then /index.html so index.html is resource full name
    if (count == 0) {
      full_name = "index.html";
    }
    else {
      //find / after www.mit.edu and eliminate all  before it
      q = i.find("/");
      f = i.substr(q+1);
      //eliminate component with ip address 
      space = f.find(" ");
      full_name = f.substr(0, space);
    }
    //use count to know resource number
    sstm << resource;
    sstm << count;
    //cout << full_name;
    //cout << "\n";
    resource_file = sstm.str();
    
    //fill resource number and full name into map
    resource_map[resource_file] = full_name;
    count = count + 1; 
  }
  file.close();
}
