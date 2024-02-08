clc
clear
close all

% Variables et constantes
l1 = 100;
l2 = 100;
l1_prime = 100;
l2_prime = 100;
d = 80;

% Ranges for X
X_values = 30:1:50;

% Cinematique inverse and animation
for X = X_values
    Y = 160;

    C_left = sqrt((X^2 + Y^2));
    gamma_left = acos((-l2^2 + l1^2 + C_left^2)/(2*l1*C_left));
    theta_left = atan2(Y, X);
    q1 = theta_left + gamma_left;

    E_right = sqrt((d-X)^2 + Y^2);
    epsilon_right = acos((-l2_prime^2 + l1_prime^2 + E_right^2)/(2*l1_prime*E_right));
    phi_right = atan2(Y, (d-X));
    q2 = pi - phi_right - epsilon_right;

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

    
    plot(PointsX, PointsY , '-o')
    title("Inverse Kinematics for 5 bars parallel SCARA robot")
    grid on
    axis equal
    xlim([-50, 150])  % Adjust the limits as needed
    ylim([-50, 200])
    pause(0.1)  % Adjust the pause duration as needed
    clf  % Clear the figure for the next iteration
end