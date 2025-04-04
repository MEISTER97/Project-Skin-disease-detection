import 'package:flutter/material.dart';

class PreviousResultsScreen extends StatelessWidget {
  final List<Map<String, dynamic>> results;

  const PreviousResultsScreen({super.key, required this.results});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Previous Results")),
      body: results.isEmpty
          ? Center(child: Text("No previous results found"))
          : ListView.builder(
        itemCount: results.length,
        itemBuilder: (context, index) {
          var result = results[index];
          return Card(
            margin: EdgeInsets.all(8),
            child: Column(
              children: [
                Image.network(result["image_url"], height: 150, fit: BoxFit.cover),
                SizedBox(height: 10),
                Text("Prediction: ${result["prediction"]}", style: TextStyle(fontSize: 18)),
                Text("Confidence: ${result["confidence"].toStringAsFixed(2)}%"),
                if (result["result_image_url"] != null)
                  Image.network(result["result_image_url"], height: 150, fit: BoxFit.cover),
                SizedBox(height: 10),
              ],
            ),
          );
        },
      ),
    );
  }
}