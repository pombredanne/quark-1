public class Crate<T> {
    Box<T> box = new Box<T>();
    Box<Integer> ibox = new Box<Integer>();
    public void set(T stuff) {
        ((this).box).set(stuff);
    }
    public T get() {
        return ((this).box).get();
    }
}