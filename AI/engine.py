import sys

from AI import logit_reg_2 as r
import tensorflow as tf
sess1 = tf.compat.v1.InteractiveSession()
print(r.x_orig, '\n-------')
# print(tf.compat.v1.Print(r.b, [r.b], "Printer: "))
init = tf.compat.v1.global_variables_initializer()

with tf.compat.v1.Session() as sess:
    sess.run(init)
    v = sess.run(r.b)
    print(v,"\n------")
    v = sess.run(r.W)
    print(v,"\n------")
    tf.print(r.b)
