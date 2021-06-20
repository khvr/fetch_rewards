#!/bin/bash
mkdir -p -- "/etc/skel/.ssh" && touch "/etc/skel/.ssh/authorized_keys"
yum update -y
yum install -y cloud-init
yum install -y xfsprogs
modprobe -v xfs
mkfs -t xfs /dev/xvdf
mkdir /data
mount /dev/xvdf /data
cp /etc/fstab /etc/fstab.bak
bash -c  'echo "/dev/xvdf       /data   xfs    defaults,nofail        0       0" >> /etc/fstab'
groupadd shared
cd / &&  mkdir sharedfolder1
chgrp shared sharedfolder1/
chmod 770 sharedfolder1
cd /data && mkdir sharedfolder2
chgrp shared sharedfolder2
chmod 770 sharedfolder2
echo adding users

adduser user1
usermod -a -G shared user1
bash -c 'echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCp0Lr2/+F/OIuabDl1d5JAiZnD5NJG+y87dJqYgZRsnNbJ//V6AtMCDNbePdfFmI2op7wBsc8MZtqYfy+80faV7v1u7j4PqDw3hp15x/JaoOsuCKHl2mN4u8y6egr8kSYe4ZxvuXWvus+5o90a2mxqM6vb9p3/3DilMC2UqyViGBUgU7mZUEDk4/t1Ze69nrs3pAGwEd/cq/so4AiRfcK1EdKCc8R6jY2ZFrxnV4mDr1ibqj6ze0TBDVByNj3rUMuSwYk6eE0VauZkPO/hDhRtIpAgwkI15wuOGXR7U2SEA7xIUyiOZvvB3PezECZ8QJPU+q5m/QX3C/fNUrVEqISFcA+fk7v3isnDOPOGWXz40dB4CPvxBA8Mpsc1h2ZAUXjnyyHfG/XiXbSTplJwftoz60fpH8qdAde29fb0nOQgTOfUa666h2p7lzBTG4L0crqHXO9Bd/taFw/p+Vk+Iecx0OUkmHiUv0LpE0vHhVuASjBUoCB0BW+XacYNvjXC6Zc= harsha@harsha-elitebook">>/home/user1/.ssh/authorized_keys'

adduser user2
usermod -a -G shared user2
bash -c 'echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDQPt2a1TTrOeqbRisvgDNWIfBDt3Rn4U5srCQn5fdmkqIY4QjE/Ydzumu7y2Tsxjp/SBfdBo2JXQWRdWE66DN4fq3LYb+Mu019Azv/EyG5FjVFN4ZDJ5AGdmkgzmxm9BTYYD1Xiq/zeNTXBRK/LnEmA849tHW3rITqqabdP8VLQhNHrwyIqdIhx1NCUD1dWU1vteLienztYuVA3d0BrX3nTwgWdEuP5RXBzLyChcZ/X8JjTebs2wzcXUjDbzGuuqQHDVt2Yqa+s9WXdpoAN8Q8aq3OEwyemCwMPLrPLjED/K8VjGUpxI5douk99LmRj7innlaOm16r8IqD/JW/oQq8+K5m2zdLOfNmDqGO562/6og1WoNi67jCLuhoBnmPvTR9JMzyoA7hIGWgLK1pcToA1nH7b1KnLaqF1O0aPxSED1CI5ipb50NCTLWmm44XwmjlQd+AP7XMkPKzEoLBJjEHc4l3Z9368fkY89ehwaBNocSd1QlE1WhvOQnxUu5cO0k= harsha@harsha-elitebook">>/home/user2/.ssh/authorized_keys'
