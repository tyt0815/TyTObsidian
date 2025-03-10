```cpp
class A
{
public:
    template <typename T>
    void F(void(T::*function)(int a, int b), T* Object)
    {
        std::function<void(int, int)> BoundFunction = 
            std::bind(function, Object, std::placeholders::_1, std::placeholders::_2);
        BoundFunction(1, 2);
    }
};

class B
{
public:
    int i = 0;
    void BF(int a, int b)
    {
        i = a + b;
        std::c[]()out << a + b;
    }
};

int main() {
    A a;
    B b;
    a.F(&B::BF, &b);
    std::cout << b.i;
    return 0;
}

```