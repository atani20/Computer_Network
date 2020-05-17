from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

def build_model(model):
    data_set_file = model +'_data_set.csv'
    model_file = model + '_model.h5'
    data_set = loadtxt(data_set_file, delimiter=',')

    X = data_set[:,0:2] # dataset[:,1:15]
    y = data_set[:,2:11]

    model = Sequential()
    model.add(Dense(15, input_dim=2, activation='tanh'))
    model.add(Dense(10, input_dim=2, activation='tanh'))
    model.add(Dense(9, activation='tanh'))

    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])  #  mean_squared_error

    model.fit(X, y, epochs=400, batch_size=40)

    model.save(model_file)
    _, accuracy = model.evaluate(X, y)
    print('Accuracy: %.2f' % (accuracy*100))

if __name__ == '__main__':
    build_model('my_conf')