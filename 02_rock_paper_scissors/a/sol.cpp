#include <iostream>
#include <map>
#include <assert.h>


constexpr char ROCK = 0;
constexpr char PAPER = 1;
constexpr char SCISSORS = 2;
const char THEIR_OFF = 'A';
const char MINE_OFF = 'X';

const std::map<char, int> scores = {
    { ROCK, 1 },
    { PAPER, 2 },
    { SCISSORS, 3 }
};

constexpr int LOSS = 0;
constexpr int DRAW = 3;
constexpr int WIN = 6;


int _eval_result(char other, char mine) {
    if (other == mine) return DRAW;
    if (mine == SCISSORS)
        return other == ROCK ?  LOSS : WIN;
    if (mine == ROCK)
        return other == PAPER ? LOSS : WIN;
    assert(mine == PAPER);
    return other == SCISSORS ? LOSS : WIN;
}


int eval(char other, char mine) {
    int r = _eval_result(other, mine);
    return r + scores.at(mine);
}


int main() {
    int score = 0;
    char other, mine;
    while ((std::cin >> other >> mine)) {
        other -= THEIR_OFF;
        mine -= MINE_OFF;
        score += eval(other, mine);
    }
    std::cout << score << std::endl;
    return 0;
}
