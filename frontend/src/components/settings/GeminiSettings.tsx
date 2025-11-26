import type { ChangeEvent, FC } from 'react';
import { Config } from '@/types/model';
import { Input } from '../ui/input';

interface GeminiSettingsProps {
  settings: Config;
  onSettingsChange: (data: Config) => void;
}

export const GeminiSettings: FC<GeminiSettingsProps> = ({
  settings,
  onSettingsChange,
}) => {
  const handleApiKeyChange = (e: ChangeEvent<HTMLInputElement>) => {
    onSettingsChange({
      ...settings,
      data: { ...settings.data, api_key: e.target.value },
    });
  };

  return (
    <Input
      id="api_key"
      name="api_key"
      label="API Key"
      type="password"
      placeholder="Enter Google API key"
      value={settings.data.api_key || ''}
      onChange={handleApiKeyChange}
    />
  );
};
