import streamlit as st
from PIL import Image
from retreive import retreive_data
from retreive import accuracy,calentropy


def main():
    st.title("Receiver Interface")
    
    # Add a file uploader for the image
    uploaded_file = st.file_uploader("Choose an embedded file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        original1_image = Image.open(uploaded_file)
        st.image(original1_image, caption="Reembedded Image", use_column_width=True)
        
        # Add radio buttons for user options
        option = st.radio("Select an option", ("Decryption", "Retrieve Secret Image", "Both"))
        
        if option == "Decryption":
            # Input fields for decryption keys
            key1 = st.text_input("Enter key 1")
            key2 = st.text_input("Enter key 2")
            
            if st.button("Decrypt"):
                # Perform decryption when the user clicks the button
                decrypted_image_path = retreive_data(uploaded_file, key1, key2,"")
                decrypted_image = Image.open(r"constructed_image.png")
                st.image(decrypted_image, caption="Constructed Image", use_column_width=True)
                st.success("Decryption image is retreived successfully!")
        
        elif option == "Retrieve Secret Image":
            # Input field for secret image key
            secret_key = st.text_input("Enter secret key")
            
            if st.button("Retrieve"):
                # Retrieve the secret image when the user clicks the button
                secret_image = retreive_data(uploaded_file,"","" ,secret_key)

                req1_image = Image.open(r"ret_secret_image.png")
                st.image(req1_image, caption="Secret Image", use_column_width=True)
                st.success("Secret is Retreived successfulyl!")
        
        elif option == "Both":
            # Input fields for decryption and secret image keys
            key1 = st.text_input("Enter key 1")
            key2 = st.text_input("Enter key 2")
            secret_key = st.text_input("Enter secret key")
            
            if st.button("Decrypt and Retrieve"):
                # Perform decryption and retrieve secret image when the user clicks the button
                decrypted_image = retreive_data(uploaded_file, key1, key2,secret_key)
                
                req2_image = Image.open(r"constructed_image.png")
                st.image(req2_image, caption="Constructed Image", use_column_width=True)
                st.success("Decryption image is retreived successfully!")
                req3_image = Image.open(r"ret_secret_image.png")
                st.image(req3_image, caption="Secret Image", use_column_width=True)
                st.success("Secret is Retreive successfulyl!")
    st.title("Image Comparison App  ")
    
    # Upload original image
    uploaded_file1 = st.file_uploader("Choose an original image file", type=["jpg", "jpeg", "png"])
    
    # Upload reconstructed image
    uploaded_file2 = st.file_uploader("Choose a reconstructed image file", type=["jpg", "jpeg", "png"])

    if uploaded_file1 and uploaded_file2:
        # Open and display images
        original_image = Image.open(uploaded_file1)
        st.image(original_image, caption='Original Image', use_column_width=True)
        
        reconstructed_image = Image.open(uploaded_file2)
        st.image(reconstructed_image, caption='Reconstructed Image', use_column_width=True)

        # Calculate RMSE
        rmse = accuracy(uploaded_file1, uploaded_file2)

        max_possible_diff = 255  # Assuming 8-bit grayscale images

        # Calculate the percentage RMSE
        percentage_rmse = (rmse / max_possible_diff) * 100
       

        st.write("Rmse:", rmse)
        # Print percentage RMSE
        st.write("Percentage RMSE:", percentage_rmse)

     # Upload original image
    uploaded_file3 = st.file_uploader("Choose an Encrypted image file", type=["jpg", "jpeg", "png"])
    if uploaded_file3 :
        # Open and display images
        Encrypted_image = Image.open(uploaded_file3)
        st.image(Encrypted_image, caption='Encrypted image', use_column_width=True)
        entropy = calentropy(uploaded_file3)


        st.write("Entropy:",entropy)
if __name__ == "__main__":
    main()


