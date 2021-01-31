int main() {
    int d;
    d = f(3, 4);
    return d;
}

int f(int a, int b) {
    int c;
    c = (a + b / a * b % a - b) ? (b) : (~a ^ b & a | b);
    return c;
}
