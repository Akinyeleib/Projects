import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class RotateArray2 {

	static void rotateArray (Integer [] arr, int count) {
		List <Integer> list1 = new ArrayList<>(Arrays.asList(arr));
		count = count % arr.length; 
		System.out.format("count is %d:\t", count);
		for (int i = 0; i < count; i++) {
			Integer item = new ArrayList<>(list1).get(list1.size() - 1);
			list1.remove(item);
			list1.add(0, item);
		}
		System.out.println(list1);
	}
		
	public static void main(String[] args) {
		rotateArray(new Integer [] {10, 20, 30, 40}, 6);
		rotateArray(new Integer [] {1, 2, 3, 4, 5, 6, 7}, 3);
		rotateArray(new Integer [] {-1, -100, 3, 99}, 2);
	}

}

