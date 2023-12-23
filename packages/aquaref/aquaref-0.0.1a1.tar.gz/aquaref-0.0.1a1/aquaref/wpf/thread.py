from System.Threading import Thread, ThreadStart, ApartmentState


def Run(Window):
    thread = Thread(ThreadStart(Window))
    thread.SetApartmentState(ApartmentState.STA)
    thread.Start()
    thread.Join()
