#include <iostream>
#include <fstream>
#include <thread>

using namespace std;

int main() {
    cout << "Starting test cpp" << endl;
    {
        ofstream o("test000.png");
        o << "test000 image" << endl;
    }
    {
        ofstream o("log");
        o << "test log" << endl;
    }
    cerr << "Error test" << endl;
    std::this_thread::sleep_for(std::chrono::seconds(600));
    cout << "finished" << endl;
}
