/**
 * oscP5sendreceive by andreas schlegel
 * example shows how to send and receive osc messages.
 * oscP5 website at http://www.sojamo.de/oscP5
 */

import oscP5.*;
import netP5.*;

OscP5 oscP5;
NetAddress myRemoteLocation;

ArrayList <dataPoint> datapoints = new ArrayList<dataPoint>();
int numLandmarks = 6;
float[] BBoxPos = new float[4]; 


void setup() {
  size(800, 600);
  //frameRate(25);
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this, 6200);

  /* myRemoteLocation is a NetAddress. a NetAddress takes 2 parameters,
   * an ip address and a port number. myRemoteLocation is used as parameter in
   * oscP5.send() when sending osc packets to another computer, device,
   * application. usage see below. for testing purposes the listening port
   * and the port of the remote location address are the same, hence you will
   * send messages back to this sketch.
   */
  myRemoteLocation = new NetAddress("10.2.4.20", 7700);

  for (int i=0; i<numLandmarks; i++) {
    datapoints.add(new dataPoint(i, 0, 0, 0, 0));
  }
}


void draw() {
  background(0);
  
  // Draw Bounding box
  stroke(255);
  strokeWeight(2);
  noFill();
  rect( BBoxPos[0], BBoxPos[1], BBoxPos[2], BBoxPos[3]);

  // Draw landmarks right eye, left eye, nose, mouth, right ear, left ear
  for (dataPoint dp : datapoints) {
    dp.draw();
  }
}




/* incoming osc message are forwarded to the oscEvent method. */
void oscEvent(OscMessage theOscMessage) {
  /* print the address pattern and the typetag of the received OscMessage */
  print("### received an osc message.");
  print(" addrpattern: "+theOscMessage.addrPattern());
  println(" typetag: "+theOscMessage.typetag());
  println("length: "+theOscMessage.typetag().length());
  // id - x - y -z - visibility - presence

  // Get Bounding obx x,y,width,height 
  BBoxPos[0] =  map(theOscMessage.get(0).floatValue(),0,1,0,width);
  BBoxPos[1] =  map(theOscMessage.get(1).floatValue(),0,1,0,height);
  BBoxPos[2] =  map(theOscMessage.get(2).floatValue(),0,1,0,width);
  BBoxPos[3] =  map(theOscMessage.get(3).floatValue(),0,1,0,height);

  // 6 landmarks
  for (int i=0; i<numLandmarks; i++) {

    int index = 4 +  i * 2;
    
    float x = (float) theOscMessage.get(index).floatValue();
    float y = (float) theOscMessage.get(index+1).floatValue();
     
    dataPoint dp = datapoints.get(i);
    dp.update(i, x, y);
  }
}

class dataPoint {

  PVector pos;
  float vis;
  
  int id;


  dataPoint(int _id, float x, float y, float z, float v) {
    id = _id;
    pos = new PVector(x, y, z);
    vis = v;
   
  }

  void draw() {
    
    float x = map(pos.x,0,1,0,width);
    float y = map(pos.y,0,1,0,height);
    
    noStroke();
    fill(255);
    circle(x, y, 20);
  }

  void update(int id, float x, float y) {
    pos.set(x, y);
    
  }

  void update(int id, float x, float y, float z, float v) {
    pos.set(x, y, z);
    vis = v;
    
  }
}
