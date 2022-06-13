import 'package:flutter/material.dart';
import 'package:hop_hui_online/colors.dart';

void main() {
  runApp(const MaterialApp(
    home: Scaffold(
      body: MyApp(),
    ),
  ));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    return Container(
      width: size.width,
      height: size.height,
      alignment: Alignment.center,
      color: PRIMARY_BACKGROUND,
      child: Stack(
        alignment: Alignment.center,
        children: [
          Positioned(
            bottom: 0,
            child: Container(
              alignment: Alignment.center,
              decoration: const BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(50),
                      topRight: Radius.circular(50))),
              width: size.width,
              height: size.height * 0.75,
              child: const Text("hello"),
            ),
          )
        ],
      ),
    );
  }
}
