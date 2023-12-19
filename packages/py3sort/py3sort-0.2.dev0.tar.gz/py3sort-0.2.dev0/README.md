# Py3Sort

Py3Sort is a Python package providing a comprehensive suite of efficient sorting algorithms. Designed to offer developers a wide array of sorting techniques, Py3Sort simplifies the process of organizing data structures with its collection of well-implemented algorithms.

## Installation

You can install Py3Sort via pip:

```bash
pip install py3sort
```

## Usage

To utilize Py3Sort in your Python scripts, simply import the desired sorting algorithms:

```python
from py3sort import bubble_sort, insertion_sort, merge_sort, selection_sort, heap_sort, quick_sort

unsorted_list = [5, 2, 9, 1, 5, 6]

# Sort using Bubble Sort
sorted_list = bubble_sort(unsorted_list)
print("Sorted using Bubble Sort:", sorted_list)

# Sort using Insertion Sort
sorted_list = insertion_sort(unsorted_list)
print("Sorted using Insertion Sort:", sorted_list)

# Use other sorting algorithms similarly
```

## Included Sorting Algorithms

Py3Sort includes the following sorting algorithms:

- **Bubble Sort:** Iteratively sorts elements by comparing adjacent elements and swapping them if they are in the wrong order.
- **Insertion Sort:** Builds the final sorted array one item at a time, inserting each element into its correct position.
- **Merge Sort:** Employs the divide-and-conquer strategy to recursively divide the list into smaller parts, sorts them, and merges them back in order.
- **Selection Sort:** Repeatedly selects the minimum element from the unsorted part and places it at the beginning.
- **Heap Sort:** Utilizes a binary heap data structure to sort elements by constructing a heap and successively removing the maximum element.
- **Quick Sort:** Divides the list into smaller sublists based on a pivot element, and recursively sorts sublists around the chosen pivot.

## Contribution

Contributions to Py3Sort are welcome! If you have ideas for enhancements or find any issues, feel free to open an issue or create a pull request on the [GitHub repository](https://github.com/Ashhad776/py3sort).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

The Py3Sort project draws inspiration from various sources and contributors in the field of sorting algorithms. A big thank you to all those who have shared their knowledge and insights!
```

This README.md provides installation instructions, usage examples, details about the included sorting algorithms, guidance for contributions, license information, and acknowledgments. Customize it further if needed, add badges, or include more detailed examples or benchmarks if necessary for your users!