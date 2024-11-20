import rclpy
from rclpy.node import Node
import customtkinter as ctk
import numpy as np
import cv2 as cv
from PIL import Image
from sensor_msgs.msg import Image as Image_msg
from cv_bridge import CvBridge
from project_interfaces.srv import PromptJanice


class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(PromptJanice, 'send_prompt')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = PromptJanice.Request()

    def send_request(self, prompt):
        self.req.prompt = prompt
        return self.cli.call_async(self.req)


class Interface(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self._text = ctk.StringVar()
        self._configure_widget()
        self._draw_widgets()

    def _configure_widget(self):  # configures itself
        self.configure(fg_color="#e5e7eb")
        self.configure(border_width=1)
        self.configure(border_color="light gray")

    def _draw_widgets(self):
        self.DEFAUL_IMAGE = np.zeros((1280, 720, 3), np.uint8)
        self.im = Image.fromarray(
            cv.cvtColor(self.DEFAUL_IMAGE, cv.COLOR_BGR2RGB)
        )
        self.im_widget = ctk.CTkImage(self.im, size=(640, 480))

        self.label = ctk.CTkLabel(self, text="", image=self.im_widget)
        self.label.pack(pady=20, padx=0, expand=False)

        self.chatbox = ctk.CTkTextbox(
            self, height=300, width=610, state="disabled", wrap=ctk.WORD
        )
        self.chatbox.pack(pady=0, padx=0, expand=False)

        self.chatbox.tag_config("janise", foreground="blue")
        self.chatbox.tag_config("worker", foreground="green")

        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(pady=20)

        self.entry = ctk.CTkEntry(
                self.menu_frame, placeholder_text="Write here...",
                height=38, width=450, border_width=1, border_color="#9ca3af",
                textvariable=self._text)
        self.entry.grid(row=1, column=0, padx=10)
        self.entry.focus()

        self.btn = ctk.CTkButton(
                self.menu_frame, text="SEND", border_spacing=10,
                command=self._send_msg)
        self.btn.grid(row=1, column=1, padx=10)

    def _send_msg(self):
        self._insert_msg(self._text.get())

        self.btn.configure(
            state="disabled", fg_color="#B22222", text="Processing"
        )
        self.entry.configure(state="disabled")
        request = self._text.get()
        self._text.set("")
        self.update()

        minimal_client = MinimalClientAsync()
        future = minimal_client.send_request(request)
        rclpy.spin_until_future_complete(minimal_client, future)
        self._insert_msg(future.result().message, is_janise=True)
        self.after(0, self._reset)

    def _reset(self):
        self.btn.configure(state="normal", fg_color="#3B8ED0", text="SEND")
        self.entry.configure(state="normal")
        self.entry.focus()

    def _insert_msg(self, msg, is_janise=False):
        self.chatbox.configure(state="normal")
        if is_janise:
            self.chatbox.insert(ctk.END, "Janise: ", tags="janise")
        else:
            self.chatbox.insert(ctk.END, "You: ", tags="worker")
        self.chatbox.insert(ctk.END, f"{msg}\n")
        self.chatbox.see("end")
        self.chatbox.configure(state="disabled")


class ImageSubscriber(Node):
    def __init__(self, root):
        super().__init__("image_subscriber")
        self.subscription = self.create_subscription(
                Image_msg,
                "video_frames",
                self.listener_callback,
                10
            )
        self.bridge = CvBridge()

        self.root = root
        self.interface = Interface(self.root)
        self.interface.pack(pady=20)
        self.root.after(100, self.update_tkinter)

    def listener_callback(self, data):
        self.get_logger().info("received image")
        current_frame = self.bridge.imgmsg_to_cv2(data)
        self.update_image(current_frame)

    def update_tkinter(self):
        rclpy.spin_once(self, timeout_sec=0.1)  # Non-blocking ROS spin

        self.root.after(100, self.update_tkinter)

    def update_image(self, data):
        self.im = Image.fromarray(cv.cvtColor(data, cv.COLOR_BGR2RGB))
        self.im_widget = ctk.CTkImage(self.im, size=(640, 480))
        self.interface.label.configure(image=self.im_widget)


def main(args=None):
    rclpy.init(args=args)
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    image_subscriber = ImageSubscriber(root=root)

    root.mainloop()
    image_subscriber.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
