#include <iostream>
#include <map>
#include <assert.h>


constexpr char ROCK = 0;
constexpr char PAPER = 1;
constexpr char SCISSORS = 2;
const char THEIR_OFF = 'A';

const std::map<char, int> scores = {
    { ROCK, 1 },
    { PAPER, 2 },
    { SCISSORS, 3 }
};

constexpr int LOSS = 0;
constexpr int DRAW = 3;
constexpr int WIN = 6;


int eval(char other, char result) {
    if (result == 'Y')
        return DRAW + scores.at(other);
    if (result == 'X')
        return LOSS + scores.at((other + 2) % 3);
    char mine = (other + 1) % 3;
    return WIN + scores.at(mine);
}


int main() {
    int score = 0;
    char other, result;
    while ((std::cin >> other >> result)) {
        other -= THEIR_OFF;
        score += eval(other, result);
    }
    std::cout << score << std::endl;
    return 0;
}
