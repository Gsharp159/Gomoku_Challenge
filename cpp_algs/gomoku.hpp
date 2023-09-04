#include <iostream>
using namespace std;

const int BOARD_SIZE = 13;
int board[BOARD_SIZE][BOARD_SIZE];

void init_board() {
    for (int i = 0; i < 169; i++) {
        board[i / BOARD_SIZE][i % BOARD_SIZE] = 0;
    }
}

void print_board(int _board[BOARD_SIZE][BOARD_SIZE]) {
    for (int i = 0; i < (sizeof(_board) * sizeof(_board[0])); i++) {
        if (i % 13 == 0) {
            cout << endl;
        }
        cout << _board[i / BOARD_SIZE][i % BOARD_SIZE] << ' ';
    }
    
}

int checkLine(int line[BOARD_SIZE], int color) {
    int longest = 0;
    int current = 0;
    for (int i = 0; i <= BOARD_SIZE; i++) {
        if (line[i] == color) {
            current++;
        } else {
            longest = max(current, longest);
            current = 0;
        }
    }
    return longest;
}

int longestSequential(int _board[BOARD_SIZE][BOARD_SIZE], int color) {
    //check rows
    int longest = 0;
    for (int i = 0; i < BOARD_SIZE; i++) {
        //cout << "row: " << i << " " << checkLine(_board[i], 1) << endl;
        longest = max(checkLine(_board[i], color), longest);
    }
    //return longest;

    //transpose and find longest horizontal
    int transposed[13][13];
    for (int row = 0; row < BOARD_SIZE; row++) {
        for (int col = 0; col < BOARD_SIZE; col++) {
            transposed[col][row] = _board[row][col];
        }
    }
    longest = 0;
    for (int i = 0; i < BOARD_SIZE; i++) {
        //cout << "row: " << i << " " << checkLine(_board[i], 1) << endl;
        longest = max(checkLine(transposed[i], color), longest);
    }
    //return longest;

    //positive diagonal
    int rotated[BOARD_SIZE * 2 - 1][BOARD_SIZE];
    for (int i = 0; i < 25; i++) {
        for (int k = 0; k < 13; k++) {
            rotated[i][k] = 0;
        }
    }

    int a, b;
    for (int i = 0; i < BOARD_SIZE * 2 - 1; i++) {
            if (i > BOARD_SIZE) {
                a = BOARD_SIZE;
            } else {
                a = i;
            }
        for (int k = 0; k <= a; k++) {
            rotated[i][k] = _board[a - k][i - k];
            //cout << a-k << " " << k;
        }

    }

    for (int i = 0; i < 25; i++) {
        for (int k = 0; k < 13; k++) {
            cout << rotated[i][k] << " ";
        }
        cout << endl;
    }

    cout << "pboard";
    print_board(rotated);

    



}

bool checkWin(int _board[BOARD_SIZE][BOARD_SIZE], int color) {return 0;}

int score(int _board[BOARD_SIZE][BOARD_SIZE], int color) {return 0;}

void place(int _board[BOARD_SIZE][BOARD_SIZE], int color, int coords[2]) {
    _board[coords[0]][coords[1]] = color;
}
