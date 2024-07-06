import streamlit as st
from PIL import Image
from sender import encrypt_image
from embbed import embed_data

def main():
    st.title("Sender Interface")
    
    # Add a file uploader for the image
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        original_image = Image.open(uploaded_file)
        st.image(original_image, caption="Original Image", use_column_width=True)
        
        # Add a button for encryption
        if st.button("Encrypt"):
            # Perform encryption when the user clicks the button
            encrypted_image_path = encrypt_image(uploaded_file)
            st.success("Encryption successful!")
            # Display the encrypted image
            encrypted_image = Image.open(r"encrypted_image.png")
            st.image(encrypted_image, caption="Encrypted Image", use_column_width=True)






    # Add a secret file uploader for the image
    embedencry_file = st.file_uploader("Choose an encypted  file", type=["jpg", "jpeg", "png"])

    embed_file = st.file_uploader("Choose an secret file", type=["jpg", "jpeg", "png"])
    
    if embed_file and embedencry_file is not None:
        # Display the secret image
        embed_image = Image.open(embed_file)
        st.image(embed_image, caption="Embed Image", use_column_width=True)

        embedencry_image = Image.open(embedencry_file)
        st.image(embedencry_image, caption="Embedencry Image", use_column_width=True)
        
        # Add a button for embed
        if st.button("Embedd"):
            # Perform encryption when the user clicks the button
            embed_image_path = embed_data(embedencry_file,embed_file)
            st.success("Embedding successful!")
            # Display the encrypted image
            embed_image = Image.open(r"reembbedded_image.png")
            st.image(embed_image, caption="ReEmbedded Image", use_column_width=True)



if __name__ == "__main__":
    main()