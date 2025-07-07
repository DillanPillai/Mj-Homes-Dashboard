
export const DashboardFooter = () => {
  return (
    <footer className="bg-white border-t border-gray-200 px-6 py-4">
      <div className="flex flex-col sm:flex-row items-center justify-between text-sm text-gray-500">
        <div className="flex items-center space-x-4">
          <span>Last Updated: {new Date().toLocaleDateString()} at {new Date().toLocaleTimeString()}</span>
          <span>Version 2.1.0</span>
        </div>
        <div className="flex items-center space-x-4 mt-2 sm:mt-0">
          <span>Contact: support@mjhome.co.nz</span>
          <span>© 2025 MJ Home</span>
        </div>
      </div>
    </footer>
  );
};
