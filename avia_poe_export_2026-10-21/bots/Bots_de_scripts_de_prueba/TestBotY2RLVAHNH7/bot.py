# poe: name=Image-Comparison

class ImageComparison:
    def run(self):
        prompt = poe.query.text

        if not prompt:
            raise poe.BotError("Please provide a description for the image you want to generate.")

        with poe.start_message() as msg:
            msg.write(f"Generating images with your prompt: *{prompt}*\n\n")

        # Generate images in parallel for efficiency
        gpt_response, nano_response = poe.parallel(
            lambda: poe.call("GPT-Image-1", prompt),
            lambda: poe.call("Nano-Banana", prompt, parameters={"image_only": True})
        )

        # Display GPT-Image-1 result
        with poe.start_message() as msg:
            msg.write("**GPT-Image-1:**\n\n")
            if gpt_response.last.attachments:
                msg.add_attachment(gpt_response.last.attachments[0])

        # Display Nano-Banana result
        with poe.start_message() as msg:
            msg.write("**Nano-Banana:**\n\n")
            if nano_response.last.attachments:
                msg.add_attachment(nano_response.last.attachments[0])

if __name__ == "__main__":
    bot = ImageComparison()
    bot.run()

