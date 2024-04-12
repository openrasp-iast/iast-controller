export function timestampToDateTime(timestamp: number): string {
  if (isNaN(timestamp)) return ''

  const date = new Date(timestamp * 1000)
  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  const seconds = date.getSeconds().toString().padStart(2, '0')

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

export function getTimestamp(): number {
  return Date.now()
}

export function isOnline(timestamp: number): boolean {
  if (timestamp > Math.round(getTimestamp() / 1000) - 60 * 3) {
    return true
  } else {
    return false
  }
}

export function convertUTCStringToLocaleString(utcDateString: string, timeZone: string): string {
  // 创建Date对象并解析日期字符串
  const date = new Date(utcDateString)

  // 设置时区
  const options = { timeZone }

  // 使用toLocaleString方法将日期转换为字符串，使用自定义的日期和时间格式
  return date.toLocaleString('zh-CN', {
    ...options,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
