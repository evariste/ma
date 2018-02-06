
float phase[] = {0, 2*PI/3, 4*PI/3};
float cx[] = {0,0,0};
float cy[] = {0,0,0};

float x_cent = 0.0;
float y_cent = 0.0;
float alpha = 0.0;
float alpha_inc = 0.01;

float x_prev[] = {0,0,0}, y_prev[] = {0,0,0};

float x0_start, y0_start;

float seg_w = 15;
float seg_h = 5;

float xy[] = {0.0, 0.0};

int n_paths = 3;
color c1 = #ffb338;
color c2 = #027878;
color c3 = #c22326;

color cols[] = {c1, c2, c3};


String frame_patt = "frames_0/f####.png";
float r = 90, R = 150, d = 180; // 3:5 -> 3 * 2 pi LCM 300 / 100

//String frame_patt = "frames_1/f####.png";
//float r = 80, R = 160, d = 160; // 1:2 -> 1 * 2pi  LCM 100 / 100

//String frame_patt = "frames_2/f####.png";
//float r = 80, R = 100, d = 200; // 4:5 -> 4 * 2pi LCM 400 / 100

//String frame_patt = "frames_3/f####.png";
//float r = 20, R = 100, d = 150; // 1:5 -> 1 * 2pi LCM 100 / 100

//String frame_patt = "frames_4/f####.png";
//float r = 90, R = 120, d = 180; // 3:4 -> 3 * 2pi   LCM 240 / 80 

//String frame_patt = "frames_5/f####.png";
//float r = 40, R = 140, d = 120; // 2:7 -> 2 * 2pi 

int n_turns;

float alpha_max = 2 * PI;

float n_pts = 1200;

void setup(){
  size(600,600);
  
  strokeWeight(1);
  noFill();
  
  background(0);
  
  cx[0] = width / 2 - 50;
  cx[1] = width / 2 + 50;
  cy[0] = cy[1] = height /2;
  cx[2] = width/2;
  cy[2] = height/2 - 80;
  
  for (int id = 0; id < n_paths; id++){
    get_path(id, 0, xy);
    x_prev[id] = xy[0];
    y_prev[id] = xy[1];
  }
  
  loop();
  
  // Get the angle needed for a full cycle.
  int r_mult = int(r);
   //<>//
  while(r_mult % int(R) != 0){
    r_mult += int(r); //<>//
  }
  
  n_turns = r_mult / int(R);
  
  alpha_max = n_turns * 2 * PI;
  
  alpha_inc = alpha_max / n_pts;
  
}


void draw(){
  
  alpha += alpha_inc; //<>//
  
  for (int id = 0; id < n_paths; id++){
    get_path(id, alpha, xy); //<>//
    draw_seg(xy[0], xy[1], seg_w, seg_h, xy[0] - x_prev[id], xy[1] - y_prev[id], id);
    x_prev[id] = xy[0];
    y_prev[id] = xy[1];
  }
  
  if (frameCount == 1){
     x0_start = x_prev[0];
     y0_start = y_prev[0];
  }
  
   saveFrame(frame_patt);

  if (alpha >= alpha_max){
    noLoop();
    print(frameCount);
  }
  
}


void get_path(int id, float t, float[] x){
  
  
  float t0 = phase[id];
  float c = cos(t + t0);
  float s = sin(t + t0);
  float a = (R-r) + d * cos(R * t / r);
  float b = d * sin(R * t / r);
  
  x[0] = width/2 + a * c + b * s;
  x[1] = height/2 + a * s - b * c;
  
  
}



void draw_seg(float x, float y, float w, float h, float u, float v, int id){

  float theta = atan2(u, v);
  draw_seg(x, y, w, h, theta, id);
}


void draw_seg(float x, float y, float w, float h, float theta, int id){
  pushMatrix();
  pushStyle();

  noStroke();

  translate(x,y);
  rotate(-theta);
  
  //fill(255);
  fill(cols[id]);
  
  rect(-w/2, -h/2, w, h);
  stroke(150);
  line(-w/2, -h/2, -w/2, +h/2);
  line(+w/2, -h/2, +w/2, +h/2);
  
  popStyle();
  popMatrix();
}