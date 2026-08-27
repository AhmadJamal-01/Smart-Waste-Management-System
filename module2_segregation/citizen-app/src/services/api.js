import axios from 'axios';

const DETECTION_API = 'http://127.0.0.1:8001';
const REWARDS_API   = 'http://127.0.0.1:8002';

export const detectWaste = async (imageFile) => {
  try {
    const form = new FormData();
    form.append('file', imageFile);
    const res = await axios.post(
      `${DETECTION_API}/api/v1/detect?conf=0.10`, form
    );
    return res.data;
  } catch (err) {
    console.error('❌ detectWaste error:', err.response?.data || err.message);
    throw err;
  }
};

export const submitDisposal = async (phone, wasteType, wasCorrect) => {
  try {
    const res = await axios.post(`${REWARDS_API}/api/v2/disposal/submit`, {
      user_phone : phone,
      waste_type : wasteType,
      was_correct: wasCorrect,
      bin_id     : "BIN-001",
    });
    return res.data;
  } catch (err) {
    console.error('❌ submitDisposal error:', err.response?.status, err.response?.data || err.message);
    throw err;
  }
};

export const getBinGuide = async (wasteType) => {
  try {
    const res = await axios.get(
      `${REWARDS_API}/api/v2/disposal/bin-guide/${wasteType}`
    );
    return res.data;
  } catch (err) {
    console.error('❌ getBinGuide error:', err.response?.data || err.message);
    throw err;
  }
};

export const getRewards = async (phone) => {
  try {
    const res = await axios.get(`${REWARDS_API}/api/v2/rewards/${phone}`);
    return res.data;
  } catch (err) {
    console.error('❌ getRewards error:', err.response?.data || err.message);
    throw err;
  }
};

export const getLeaderboard = async () => {
  try {
    const res = await axios.get(`${REWARDS_API}/api/v2/leaderboard`);
    return res.data;
  } catch (err) {
    console.error('❌ getLeaderboard error:', err.response?.data || err.message);
    throw err;
  }
};

export const getBadges = async (userId) => {
  try {
    const res = await axios.get(`${REWARDS_API}/api/v2/badges/user/${userId}`);
    return res.data;
  } catch (err) {
    console.error('❌ getBadges error:', err.response?.data || err.message);
    throw err;
  }
};