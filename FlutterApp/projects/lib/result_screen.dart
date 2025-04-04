import 'package:flutter/material.dart';

class ResultScreen extends StatelessWidget {
  final String prediction;
  final double confidence;
  final String imageUrl;
  final String resultImageUrl;
  final double resultImageWidth;
  final double resultImageHeight;

  const ResultScreen({
    required this.prediction,
    required this.confidence,
    required this.imageUrl,
    required this.resultImageUrl,
    required this.resultImageWidth,
    required this.resultImageHeight,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Prediction Result")),
      body: SingleChildScrollView( // Wrap the Column with SingleChildScrollView
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start, // Align from the top
            children: [
              // Display the original image with resizing
              Image.network(
                imageUrl, // Using the passed image URL
                width: resultImageWidth, // Set width to match the result image width
                height: resultImageHeight, // Set height to match the result image height
                errorBuilder: (context, error, stackTrace) {
                  return Text("Failed to load image.", style: TextStyle(color: Colors.red));
                },
              ),
              SizedBox(height: 20),
              // Display prediction and confidence
              Text("Prediction: $prediction", style: TextStyle(fontSize: 20)),
              Text("Confidence: ${confidence.toStringAsFixed(2)}%", style: TextStyle(fontSize: 18)),
              SizedBox(height: 20),
              // Display the result image with the passed size
              Image.network(
                resultImageUrl, // Using the passed result image URL
                width: resultImageWidth, // Set width
                height: resultImageHeight, // Set height
                errorBuilder: (context, error, stackTrace) {
                  return Text("Failed to load result image.", style: TextStyle(color: Colors.red));
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
