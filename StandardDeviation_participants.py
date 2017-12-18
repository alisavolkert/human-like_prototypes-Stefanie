# Copyright 2017 Stefanie Müller
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import math

tmp=[61, 65, 26, 23, 22, 53, 55, 25, 26, 25, 48, 46, 61, 57, 26, 22 ,61, 63, 25, 27, 23, 28, 22]
n=23
mean=0
for i in range(len(tmp)):
    mean=mean+tmp[i]
mean=float(mean)
mean=mean/n
print(" mean= ", mean)
print("2^3", math.pow(2,3))
sd=0
for i in range(len(tmp)):
    sd= sd + math.pow((tmp[i]-mean),2)
x=n
x=float(x)
x=1/x
sd=sd*x
sd=math.sqrt(sd)
print(" sd= ", sd)
