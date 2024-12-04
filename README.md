# Height Monitoring in Metal Printing Using CCD Camera and Machine Learning

### Objective
1. Extract and visualize the metal part from CCD camera images during 3D printing.
2. Identify height variations caused by excessive powder flow or improper nozzle positioning.
3. Generate a height profile for each layer and export it as a CSV file for further analysis.

### Key Features
1. Color Masking: Different color spaces (RGB, LAB, Grayscale, and white contours) are used to segment the metal part.
2. Height Monitoring: Calculates the height of the metal part at specific x-coordinates using pixel-to-length conversion.
3. Layer Analysis: Tracks layer transitions to identify the printing state.
4. Data Export: Saves calculated heights for each layer as a CSV file.

## Algorithm Workflow
### Input:
- CCD camera images of the metal printing process stored in a folder using `os.listdir`.
- User-defined x-coordinates to calculate heights.

### Process Images:
- Read and sort all image files from the specified folder.
- For each image: Determine Printing State:
- Check if printing is active by analyzing pixel brightness thresholds (is_printing()).
- to extract Metal Part convert the image to grayscale and LAB color spaces.
- Apply multiple masks (RGB, LAB, Grayscale, and white contour) to isolate metal regions (extract_object()).
- Identify the largest contour to refine the extracted metal part.
  
### Height Calculation:
- For the extracted metal part: Measure the pixel height at the user-defined x-coordinates.
- Convert pixel measurements to real-world heights using a scale factor (13.4 mm / 394 pixels) (find_extracted_object_height()).
- Detect layer transitions based on changes in the printing state.
- Record the heights and layer numbers for each captured frame.

### Output:
- Save the calculated heights and corresponding layer numbers to a CSV file (heights1.csv) for further analysis (write_lists_to_csv()).
