from djitellopy import Tello
import time

def check_tello_connection():
    try:
        tello = Tello()
        tello.connect()
        
        battery = tello.get_battery()
        print(f'Connected to Tello! Battery level: {battery}%')

        if battery > 0:
            print("Tello connection is successful!")
            return tello, battery  # Return the Tello instance and battery level
        else:
            print("Connected but unable to retrieve battery info. Check the drone.")
            return None, 0

    except Exception as e:
        print("Failed to connect to Tello.")
        print(f"Error: {e}")
        return None, 0


def calibrate_imu(tello):
    print("Calibrating IMU...")
    try:
        tello.send_control_command("rc 0 0 0 0")  # Reset any inputs
        tello.send_control_command("emergency")   # Reset drone
        time.sleep(2)
        print("IMU calibration complete.")
    except Exception as e:
        print(f"IMU calibration failed: {e}")


def fly_tello(tello):
    try:
        battery = tello.get_battery()
        if battery < 30:
            print("Battery too low for flight. Please charge the drone.")
            return

        print("Taking off...")
        response = tello.send_control_command("takeoff")

        if response != 'ok':
            print("Takeoff failed. Recalibrating IMU and retrying...")
            calibrate_imu(tello)
            response = tello.send_control_command("takeoff")

            if response != 'ok':
                print("Takeoff unsuccessful after recalibration.")
                return
        
        print("Hovering for 5 seconds...")
        time.sleep(5)

        print("Flying forward 200 cm...")
        tello.move_forward(200)

        print("Rotating 180 degrees...")
        tello.rotate_clockwise(180)

        print("Flying forward 200 cm...")
        tello.move_forward(200)

        print("Rotating 180 degrees...")
        tello.rotate_clockwise(180)

        print("Landing...")
        tello.land()

        print("Flight completed successfully!")

    except Exception as e:
        print("An error occurred during flight.")
        print(f"Error: {e}")
        calibrate_imu(tello)  # Recalibrate if flight fails mid-air
        tello.emergency()  # Stop motors immediately if something goes wrong


if __name__ == "__main__":
    tello, battery = check_tello_connection()
    
    if tello is not None and battery > 30:
        fly_tello(tello)
    else:
        print("Flight aborted due to connection issues or low battery.")