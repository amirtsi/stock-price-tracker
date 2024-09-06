window.URL.createObjectURL = () => {};

// Mocking HTMLCanvasElement.getContext
HTMLCanvasElement.prototype.getContext = () => {
  return {}; 
};
