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
                padding: const EdgeInsets.symmetric(vertical: 25),
                alignment: Alignment.topCenter,
                decoration: const BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.only(
                        topLeft: Radius.circular(50),
                        topRight: Radius.circular(50))),
                width: size.width,
                height: size.height * 0.75,
                child: SingleChildScrollView(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Hui_Group_Item(size: size),
                      Hui_Group_Item(size: size),
                      Hui_Group_Item(size: size),
                      Hui_Group_Item(size: size),
                      Hui_Group_Item(size: size),
                    ],
                  ),
                )),
          )
        ],
      ),
    );
  }
}

class Hui_Group_Item extends StatelessWidget {
  const Hui_Group_Item({
    Key? key,
    required this.size,
  }) : super(key: key);

  final Size size;

  @override
  Widget build(BuildContext context) {
    return Container(
        margin: const EdgeInsets.only(bottom: 20),
        alignment: Alignment.topCenter,
        padding: const EdgeInsets.all(15),
        decoration: const BoxDecoration(
            color: Colors.grey,
            borderRadius: BorderRadius.all(Radius.circular(15))),
        width: size.width * 0.9,
        child: Column(children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                "Hụi phố phường",
                style: TextStyle(
                    fontSize: size.height * 0.028, fontWeight: FontWeight.bold),
              ),
              IconButton(
                iconSize: size.height * 0.035,
                icon: Icon(Icons.favorite),
                color: Colors.red,
                onPressed: () {},
              )
            ],
          ),
          const SizedBox(height: 15),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("40.000d",
                  style: TextStyle(
                      fontSize: size.height * 0.025,
                      fontWeight: FontWeight.bold,
                      color: PINK_TEXT)),
              TextButton(
                style: TextButton.styleFrom(
                    padding: const EdgeInsets.symmetric(
                        vertical: 15, horizontal: 25),
                    primary: Color.fromARGB(217, 255, 255, 255),
                    backgroundColor: GREEN),
                child: Text("Active"),
                onPressed: () {},
              )
            ],
          ),
        ]));
  }
}
