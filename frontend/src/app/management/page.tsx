'use client';

import { useState, useEffect } from 'react';
import ChannelManagement from '../../components/ChannelManagement';

const ManagementPage = () => {
  return (
    <div className="min-h-screen bg-gray-900">
      <ChannelManagement />
    </div>
  );
};

export default ManagementPage;
