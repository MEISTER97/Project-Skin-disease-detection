import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';  // To pick images (use for taking a picture)
import 'package:SkinAI/result_screen.dart';
import 'previous_results_screen.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:SkinAI/utils/config.dart';



final secureStorage = FlutterSecureStorage();


class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ImagePicker _picker = ImagePicker();

  // Function to open camera and take a picture
  Future<void> _takePicture() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.camera);
    if (image != null) {
      await _uploadImage(File(image.path));
    }
  }

  // Function to open gallery and pick a photo
  Future<void> _addPhoto() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      await _uploadImage(File(image.path));
    }
  }

  // upload the image to the server and getting result
  Future<void> _uploadImage(File imageFile) async {
    final accessToken = await secureStorage.read(key: 'access_token');
    if (accessToken == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Session expired. Please log in again.")),
      );
      Navigator.pushReplacementNamed(context, '/signin');
      return;
    }

    var url = Uri.parse("$BASE_URL/api/flutter_upload/");
    var request = http.MultipartRequest('POST', url)
      ..headers['Authorization'] = 'Bearer $accessToken'
      ..headers['X-Request-Source'] = 'flutter'
      ..files.add(await http.MultipartFile.fromPath('image', imageFile.path));

    try {
      var response = await request.send().timeout(Duration(seconds: 30));

      if (response.statusCode == 200) {
        var responseBody = await response.stream.bytesToString();
        var jsonResponse = json.decode(responseBody);

        // Safely parse and fix URLs
        String imageUrl = jsonResponse['image_url'] ?? '';
        String resultImageUrl = jsonResponse['result_image_url'] ?? '';
        int resultImageWidth = jsonResponse['result_image_width'] ?? 0;
        int resultImageHeight = jsonResponse['result_image_height'] ?? 0;

        if (!imageUrl.startsWith('http')) imageUrl = '$BASE_URL$imageUrl';
        if (!resultImageUrl.startsWith('http')) resultImageUrl = '$BASE_URL$resultImageUrl';

        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => ResultScreen(
              prediction: jsonResponse['prediction'] ?? 'Unknown',
              confidence: jsonResponse['confidence'] ?? 0.0,
              imageUrl: imageUrl,
              resultImageUrl: resultImageUrl,
              resultImageWidth: resultImageWidth.toDouble(),
              resultImageHeight: resultImageHeight.toDouble(),
            ),
          ),
        );
      } else if (response.statusCode == 401) {
        throw Exception("Unauthorized. Please log in again.");
      } else {
        throw Exception('Upload failed with status code: ${response.statusCode}');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Upload failed: ${e.toString()}")),
      );
    }
  }



  //function to get previous results up to 10
  Future<List<Map<String, dynamic>>> fetchPreviousResults() async {
    final accessToken = await secureStorage.read(key: 'access_token');
    if (accessToken == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Session expired. Please log in again.")),
      );
      Navigator.pushReplacementNamed(context, '/signin');
      return [];
    }

    var url = Uri.parse("$BASE_URL/api/flutter_results/");
    try {
      var response = await http.get(
        url,
        headers: {
          "Authorization": "Bearer $accessToken",
          "X-Request-Source": "flutter_previous_results"
        },
      );

      if (response.statusCode == 200) {
        var jsonResponse = json.decode(response.body);
        return List<Map<String, dynamic>>.from(jsonResponse['results']);
      } else if (response.statusCode == 401) {
        throw Exception("Unauthorized. Please sign in again.");
      } else {
        throw Exception("Failed to load previous results");
      }
    } catch (e) {
      throw Exception("Error fetching results: ${e.toString()}");
    }
  }



// Function to navigate to the previous results screen
  void _goToPreviousResults() async {
    try {
      List<Map<String, dynamic>> results = await fetchPreviousResults();
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => PreviousResultsScreen(results: results),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Failed to fetch results: ${e.toString()}")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Home Screen")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              // Center buttons horizontally
              children: [
                ElevatedButton(
                  onPressed: _takePicture,
                  child: Text("Take a Picture"),
                ),
                SizedBox(width: 20), // Space between buttons
                ElevatedButton(
                  onPressed: _addPhoto,
                  child: Text("Add Photo"),
                ),
              ],
            ),
            SizedBox(height: 20), // Space between rows

            // Button to see previous results
            ElevatedButton(
              onPressed: _goToPreviousResults,
              child: Text("See Previous Results"),
            ),
          ],
        ),
      ),
    );
  }

}
