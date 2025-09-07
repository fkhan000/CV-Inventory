import {apiClient} from "./apiClient.js";

export const registerUser = async (userName, emailAddress) => {
    const data = {
      user_name: userName,
      email_address: emailAddress,
    };

    const response = await apiClient.post("/register_user", data);
    console.log(response);
    return response;
};

export const login = async (emailAddress) => {
  try {
    const response = await apiClient.post("/fetch_user", { email_address: emailAddress });

    if (response.status === 200) {
      if (!response.data || response.data.length === 0) {
        throw new Error("Invalid login credentials provided");
      }

      const user = response.data;
      return {
        id: user.user_id,
        emailAddress: user.email_address,
        userName: user.user_name,
      };
    } else {
      throw new Error("Error logging in");
    }
  } catch (err) {
    throw err;
  }
};
