#pragma GCC target ("avx2")
#pragma GCC optimize ("O3")
#pragma GCC optimize("Ofast")
#pragma GCC optimize ("unroll-loops")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,tune=native")

#include <iostream>
#include <set>
#include <vector>
#include <cassert>
#include <iomanip>
#include <numeric>


using Coord = std::pair<int, int>;
using Block = std::vector<Coord>;
using ull = unsigned long long;

const Block b_minus = { {0,0}, {0,1}, {0,2}, {0,3} };
const Block b_plus = { {0,1}, {1,0}, {1,1}, {1,2}, {2,1} };
const Block b_l = { {0,2}, {0,1}, {0,0}, {1,2}, {2,2} };
const Block b_i = { {0,0}, {1,0}, {2,0}, {3,0} };
const Block b_hash = { {0,0}, {0,1}, {1,0}, {1,1} };
const Block blocks[5] = { b_minus, b_plus, b_l, b_i, b_hash };


struct Arena {
    const int width;
    int height = 0;
    std::set<Coord> fixed;

    explicit Arena(int width) : width(width) {}

    void move(Block& b, int dx, int dy) {
        for (std::size_t i=0; i<b.size(); ++i) {
            b[i].first += dy;
            b[i].second += dx;
        }
    }

    Block spawn(int n) {
        auto selected = blocks[n % 5];
        int left = 200, bottom = 200;
        for (const auto& [y,x] : selected) {
            left = std::min(left, x);
            bottom = std::min(bottom, y);
        }
        const int dx = std::max(0, 2-left),
                  dy = std::max(0, 3+this->height-bottom);
        move(selected, dx, dy);
        return selected;
    }

    bool can_move(const Block& b, int dx, int dy) {
        for (const auto& pos : b) {
            Coord new_pos = { pos.first + dy, pos.second + dx };
            if (this->fixed.count(new_pos) || new_pos.second >= this->width || new_pos.first < 0 || new_pos.second < 0)
                return false;
        }
        return true;
    }

    void simulate(ull steps, const std::string& shifts, bool verbose = false) {
        int _block = 0, _dir = 0;

        for (ull s=0; s<steps; ++s) {
            if (s % 100 == 0 && verbose) {
                std::cout << "\rSteps: " << s << "/" << steps << "\t\t" << std::setprecision(2) << static_cast<float>(s*100) / steps << "%                      ";
            }


            auto b = spawn(_block++);
            assert(can_move(b, 0, -1));
            while (true) {
                int dx = shifts[(_dir++) % shifts.size()] == '<' ? -1 : 1;
                if (can_move(b, dx, 0)) move(b, dx, 0);

                if (can_move(b, 0, -1)) {
                    move(b, 0, -1);
                }
                else {
                    for (const auto& p : b) {
                        // if (fixed.count(p)) {
                        //     std::cerr << p.first << " " << p.second << "\n";
                        // }
                        assert(fixed.count(p) == 0);
                        this->fixed.insert(p);
                        this->height = std::max(this->height, p.first + 1);
                    }
                    // check if we have finished a whole line
                    bool ok = true;
                    for (int i=0; i<7; ++i) {
                        if (fixed.count(std::make_pair(height-1, i)) == 0)
                            ok = false;
                    }
                    if (ok) {
                        std::cout << "GGGG " << s << "\n";
                    }
                    break;
                }
            }
            // print();
            // for (auto [y,x] : fixed) {
            //     std::cout << y << "-" << x << "\n";
            // }
        }
    }

    void print() {
        std::vector<std::vector<char>> fp(height, std::vector<char>(width, '.'));
        for (auto [y,x] : fixed) fp[y][x] = '#';
        for (int i=height-1; i>=0; --i) {
            std::cout << "|";
            for (int j=0; j<width; ++j) {
                std::cout << fp[i][j];
            }
            std::cout << "|\n";
        }
        std::cout << "+";
        for (int i=0; i<width; ++i) {
            std::cout << '-';
        }
        std::cout << "+\n";
    }
};


int main() {
    const ull steps = 1000000000000ull;
    std::string dirs;
    std::cin >> dirs;

    // first determine the minimum repeated height
    ull repeated_steps = std::lcm(5, dirs.size());

    // then find it
    // for (ull rep=2; rep < 100; ++rep) {
    //     std::cout << "\r" << rep << "/" << 100 << "   ";
    //     for (ull basic=1; basic < 100; ++basic) {
    //         auto aa = Arena(7);
    //         aa.simulate(basic*repeated_steps, dirs);
    //         ull first = aa.height;
    //         auto bb = Arena(7);
    //         bb.simulate(rep*basic*repeated_steps, dirs);
    //         ull snd = bb.height;

    //         if (snd % first == 0) {
    //             std::cout << "\nFound repeating pattern: "
    //                       << basic << "[" << first << "]"
    //                       << " / "
    //                       << rep << "[" << snd << "]" << "\n";
    //             return 0;
    //         }
    //     }
    // }
    Arena(7).simulate(steps, dirs, true);

    ull repetitions = steps / repeated_steps;
    ull todo = steps % repeated_steps;

    // repetitions
    auto arena = Arena(7);
    arena.simulate(repeated_steps, dirs, true);
    ull h = arena.height;

    // the last repetition + the rest
    auto todo_arena = Arena(7);
    todo_arena.simulate(repeated_steps + todo, dirs);
    ull hh = todo_arena.height;

    // results
    std::cout << "\n" << repeated_steps << "   " << h << " " << hh << "\n";
    std::cout << h * (repetitions - 1) + hh << std::endl;
    return 0;
}