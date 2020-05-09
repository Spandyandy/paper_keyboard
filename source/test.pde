import ddf.minim.*;
import ddf.minim.analysis.*;

Minim minim;
FFT fft;
int a=0;
HashMap<Integer,String> hm = new HashMap<Integer,String>();
int numObjects = 102;
int numEdge = 1000;

Edge[] edge;
Object[] objects;

float basslimit = 0.025;  //limit value of bass RANGE: 0 - 0.03
float midlimit = 0.07;  //limit value of mid RANGE: 0.03 - 0.1
float treblelimit = 0.2; //limit value of treble RANGE: 0.1 - 0.3
float bass = 0;
float mid = 0;
float treble = 0;
float prevBass = bass;
float prevMid = mid;
float prevTreble = treble;

AudioPlayer[] songFiles;
int currSong;

void setup()
{
  size(displayWidth, displayHeight, P3D);
  minim = new Minim(this);
  hm.put(1, "workit.wav");
  hm.put(2, "doit.wav");
  hm.put(3, "harder.wav");
  hm.put(4, "stronger.wav");
  
  edge = new Edge[numEdge];
  for(int i = 0; i < numEdge; i+= 4){
   edge[i] = new Edge(0, height/2, 10, height-50);
   edge[i+1] = new Edge(width, height/2, 10, height-50); 
   edge[i+2] = new Edge(width/2, height, width-50, 10); 
   edge[i+3] = new Edge(width/2, 0, width-50, 10); 
  } 
  
  objects = new Object[numObjects];
  for (int i = 0; i < numObjects; i++) {
   objects[i] = new Object(); 
  }
  setupSongs();
  loop();
}

void draw()
{
  String[] lines = loadStrings("./list.txt");
  if(lines.length != a) {
      songFiles[currSong].pause();
      songFiles[currSong].rewind();
      currSong = Integer.parseInt(lines[lines.length-1]) - 1;
      songFiles[currSong].play();
      println(lines[lines.length-1]);
  }
  if (!songFiles[currSong].isPlaying()){
    songFiles[currSong].pause();
    songFiles[currSong].rewind();
  }
      
  fft = new FFT(songFiles[currSong].bufferSize(), songFiles[currSong].sampleRate());
  fft.forward(songFiles[currSong].mix);
  
  prevBass = bass;
  prevMid = mid;
  prevTreble = treble;
  bass = 0;
  mid = 0;
  treble = 0;
  for(int i = 0; i < fft.specSize()*basslimit; i++)
  {
    bass += fft.getBand(i);
  }
  for(int i = (int)(fft.specSize()*basslimit); i < fft.specSize()*midlimit; i++)
  {
    mid += fft.getBand(i);
  }
  for(int i = (int)(fft.specSize()*midlimit); i < fft.specSize()*treblelimit; i++)
  {
    treble += fft.getBand(i);
  }
  float total = 0.4*bass+0.8*mid+treble;
  background(bass/100, mid/100, treble/100);
  equalizer3(total);
  for(int i = 0; i < numObjects; i++)
  {
    float bandVal = fft.getBand(i);
    objects[i].display(bass, mid, treble, bandVal, total, true, false);
  }
  
  //border edges
  for(int i = 0; i < numEdge; i++)
  {
    edge[i].display(bass, mid, treble, total);
  }
  
  a = lines.length;
}

void setupSongs() {
  songFiles = new AudioPlayer[hm.size()];
  for (int i = 1; i<=songFiles.length; i++) {
    songFiles[i - 1] = minim.loadFile(hm.get(i), 1024);
  }
}
