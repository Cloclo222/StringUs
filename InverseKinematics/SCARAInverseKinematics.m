clc
clear
close all

% Variables et constantes

l1 = 142.825;
l2 = 160;
l1_prime = 142.825;
l2_prime = 160;
d = 218.702;

% Commande
X = (d/2)+30;
Y = 250-60;

% Cinematique inverse

C_left = sqrt((X^2 + Y^2));
gamma_left = acos((-l2^2 + l1^2 + C_left^2)/(2*l1*C_left));
theta_left = atan2(Y, X);
q1 = theta_left + gamma_left;
q1_servo = rad2deg(q1)

E_right = sqrt((d-X)^2 + Y^2);
epsilon_right = acos((-l2_prime^2 + l1_prime^2 + E_right^2)/(2*l1_prime*E_right));
phi_right = atan2(Y, (d-X));
q2 = pi - phi_right - epsilon_right;
q2_servo = rad2deg(pi-q2)

% Representation du robot

x0 = 0;
y0 = 0;

x4 = d;
y4 = 0;

x1 = x0 + l1 * cos(q1);
y1 = y0 + l1 * sin(q1);

x3 = x4 + l1_prime * cos(q2);
y3 = y4 + l1_prime * sin(q2);

x2 = X; 
y2 = Y;

PointsX = [x0,x1,x2,x3,x4];
PointsY = [y0,y1,y2,y3,y4];

figure(1)

plot(PointsX, PointsY , '-o')
title("Inverse Kinematics for 5 bars parallel SCARA robot")
grid on




