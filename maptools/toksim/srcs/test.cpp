# include <unordered_map>
# include <iostream>
# include <string>

using namespace std;

int main(){
    unordered_map<string, int> map;
    map["this"] = 9;
    map["is"] = 8;
    map["a"] = 7;
    map["dog"] = 6;

    for(auto it : map){
        it.second -= 6;
    }

    for(auto &it : map){
        cout << it.second << endl;
    }
    return 0;
}